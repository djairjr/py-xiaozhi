import asyncio
import logging
import os
import shutil
import sys
import termios
import tty
from collections import deque
from typing import Callable, Optional

from src.display.base_display import BaseDisplay


class CliDisplay(BaseDisplay):
    def __init__(self):
        super().__init__()
        self.running = True
        self._use_ansi = sys.stdout.isatty()
        self._loop = None
        self._last_drawn_rows = 0

        # Dashboard data (top content display area)
        self._dash_status = ""
        self._dash_connected = False
        self._dash_text = ""
        self._dash_emotion = ""
        # Layout: only two areas (display area + input area)
        # Reserve two lines of input space (separator line + input line), and leave an extra line for cleaning up Chinese input overflow
        self._input_area_lines = 3
        self._dashboard_lines = 8  # The minimum number of lines in the default display area (will be dynamically adjusted according to the height of the terminal)

        # Color/Style (only takes effect under TTY)
        self._ansi = {
            "reset": "\x1b[0m",
            "bold": "\x1b[1m",
            "dim": "\x1b[2m",
            "blue": "\x1b[34m",
            "cyan": "\x1b[36m",
            "green": "\x1b[32m",
            "yellow": "\x1b[33m",
            "magenta": "\x1b[35m",
        }

        # callback function
        self.auto_callback = None
        self.abort_callback = None
        self.send_text_callback = None
        self.mode_callback = None

        # Asynchronous queue is used to process commands
        self.command_queue = asyncio.Queue()

        # Log buffering (only shown at the top of the CLI, not printed directly to the console)
        self._log_lines: deque[str] = deque(maxlen=6)
        self._install_log_handler()

    async def set_callbacks(
        self,
        press_callback: Optional[Callable] = None,
        release_callback: Optional[Callable] = None,
        mode_callback: Optional[Callable] = None,
        auto_callback: Optional[Callable] = None,
        abort_callback: Optional[Callable] = None,
        send_text_callback: Optional[Callable] = None,
    ):
        """Set the callback function."""
        self.auto_callback = auto_callback
        self.abort_callback = abort_callback
        self.send_text_callback = send_text_callback
        self.mode_callback = mode_callback

    async def update_button_status(self, text: str):
        """Update button state."""
        # Simplification: Button status is only displayed in the dashboard text
        self._dash_text = text
        await self._render_dashboard()

    async def update_status(self, status: str, connected: bool):
        """Update status (only updates the dashboard, no new rows are appended)."""
        self._dash_status = status
        self._dash_connected = bool(connected)
        await self._render_dashboard()

    async def update_text(self, text: str):
        """
        更新文本（仅更新仪表盘，不追加新行）。
        """
        if text and text.strip():
            self._dash_text = text.strip()
            await self._render_dashboard()

    async def update_emotion(self, emotion_name: str):
        """Update emoticons (only update the dashboard, no new rows will be appended)."""
        self._dash_emotion = emotion_name
        await self._render_dashboard()

    async def start(self):
        """Start an asynchronous CLI display."""
        self._loop = asyncio.get_running_loop()
        await self._init_screen()

        # Start command processing task
        command_task = asyncio.create_task(self._command_processor())
        input_task = asyncio.create_task(self._keyboard_input_loop())

        try:
            await asyncio.gather(command_task, input_task)
        except KeyboardInterrupt:
            await self.close()

    async def _command_processor(self):
        """Command processor."""
        while self.running:
            try:
                command = await asyncio.wait_for(self.command_queue.get(), timeout=1.0)
                if asyncio.iscoroutinefunction(command):
                    await command()
                else:
                    command()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Command processing error: {e}")

    async def _keyboard_input_loop(self):
        """Keyboard input loop."""
        try:
            while self.running:
                # Under TTY, fixed bottom input area reads input
                if self._use_ansi:
                    await self._render_input_area()
                    # Take over the input yourself (disable terminal echo), redraw the input line word by word, and completely solve the problem of residual Chinese first characters
                    cmd = await asyncio.to_thread(self._read_line_raw)
                    # Clean the input area (including possible Chinese line breaks) and refresh the top content
                    self._clear_input_area()
                    await self._render_dashboard()
                else:
                    cmd = await asyncio.to_thread(input)
                await self._handle_command(cmd.lower().strip())
        except asyncio.CancelledError:
            pass

    # ===== Log interception and forwarding to the display area =====
    def _install_log_handler(self) -> None:
        class _DisplayLogHandler(logging.Handler):
            def __init__(self, display: "CliDisplay"):
                super().__init__()
                self.display = display

            def emit(self, record: logging.LogRecord) -> None:
                try:
                    msg = self.format(record)
                    self.display._log_lines.append(msg)
                    loop = self.display._loop
                    if loop and self.display._use_ansi:
                        loop.call_soon_threadsafe(
                            lambda: asyncio.create_task(
                                self.display._render_dashboard()
                            )
                        )
                except Exception:
                    pass

        root = logging.getLogger()
        # Remove processors that write directly to stdout/stderr to avoid overwriting rendering
        for h in list(root.handlers):
            if isinstance(h, logging.StreamHandler) and getattr(h, "stream", None) in (
                sys.stdout,
                sys.stderr,
            ):
                root.removeHandler(h)

        handler = _DisplayLogHandler(self)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s [%(name)s] - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root.addHandler(handler)

    async def _handle_command(self, cmd: str):
        """Process the command."""
        if cmd == "q":
            await self.close()
        elif cmd == "h":
            self._print_help()
        elif cmd == "r":
            if self.auto_callback:
                await self.command_queue.put(self.auto_callback)
        elif cmd == "x":
            if self.abort_callback:
                await self.command_queue.put(self.abort_callback)
        else:
            if self.send_text_callback:
                await self.send_text_callback(cmd)

    async def close(self):
        """Turn off the CLI display."""
        self.running = False
        print("\nClose application...\n")

    def _print_help(self):
        """Write help information to the top content display area instead of printing it directly."""
        help_text = "r: start/stop | x: interrupt | q: exit | h: help | other: send text"
        self._dash_text = help_text

    async def _init_screen(self):
        """Initialize the screen and render two areas (display area + input area)."""
        if self._use_ansi:
            # Clear the screen and return to the upper left
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.flush()

        # Initial full-scale drawing
        await self._render_dashboard(full=True)
        await self._render_input_area()

    def _goto(self, row: int, col: int = 1):
        sys.stdout.write(f"\x1b[{max(1,row)};{max(1,col)}H")

    def _term_size(self):
        try:
            size = shutil.get_terminal_size(fallback=(80, 24))
            return size.columns, size.lines
        except Exception:
            return 80, 24

    # ====== Raw mode support to avoid Chinese residue ======
    def _read_line_raw(self) -> str:
        """Read a line using raw mode: turn off echo, read character by character and echo it yourself, avoid wide character (Chinese) deletion residue by redrawing the entire line."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            buffer: list[str] = []
            while True:
                ch = os.read(fd, 4)  # Read up to 4 bytes, enough to cover common UTF-8 Chinese
                if not ch:
                    break
                try:
                    s = ch.decode("utf-8")
                except UnicodeDecodeError:
                    # If the complete UTF-8 cannot be formed, continue reading until it can be decoded.
                    while True:
                        ch += os.read(fd, 1)
                        try:
                            s = ch.decode("utf-8")
                            break
                        except UnicodeDecodeError:
                            continue

                if s in ("\r", "\n"):
                    # Enter: line feed, end input
                    sys.stdout.write("\r\n")
                    sys.stdout.flush()
                    break
                elif s in ("\x7f", "\b"):
                    # Backspace: delete a Unicode character
                    if buffer:
                        buffer.pop()
                    # Redraw the entire line to avoid Chinese wide character residues
                    self._redraw_input_line("".join(buffer))
                elif s == "\x03":  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    buffer.append(s)
                    self._redraw_input_line("".join(buffer))

            return "".join(buffer)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _redraw_input_line(self, content: str) -> None:
        """Clear the input line and rewrite the current content to ensure that no Chinese characters are left behind."""
        cols, rows = self._term_size()
        separator_row = max(1, rows - self._input_area_lines + 1)
        first_input_row = min(rows, separator_row + 1)
        prompt = "enter:" if not self._use_ansi else "\x1b[1m\x1b[36mInput:\x1b[0m"
        self._goto(first_input_row, 1)
        sys.stdout.write("\x1b[2K")
        visible = content
        # Avoid more than one line causing line breaks
        max_len = max(1, cols - len("enter:") - 1)
        if len(visible) > max_len:
            visible = visible[-max_len:]
        sys.stdout.write(f"{prompt}{visible}")
        sys.stdout.flush()

    async def _render_dashboard(self, full: bool = False):
        """Update content display in the top fixed area without touching the bottom input row."""

        # Truncate long text to avoid line breaks tearing the interface
        def trunc(s: str, limit: int = 80) -> str:
            return s if len(s) <= limit else s[: limit - 1] + "…"

        lines = [
            f"Status: {trunc(self._dash_status)}",
            f"Connection: {'Connected' if self._dash_connected else 'Not connected'}",
            f"Expression: {trunc(self._dash_emotion)}",
            f"Text: {trunc(self._dash_text)}",
        ]

        if not self._use_ansi:
            # Degenerate: only print last line of status
            print(f"\r{lines[0]}        ", end="", flush=True)
            return

        cols, rows = self._term_size()

        # Number of available display lines = total number of terminal lines - number of input area lines
        usable_rows = max(5, rows - self._input_area_lines)

        # A little style function
        def style(s: str, *names: str) -> str:
            if not self._use_ansi:
                return s
            prefix = "".join(self._ansi.get(n, "") for n in names)
            return f"{prefix}{s}{self._ansi['reset']}"

        title = style("Xiaozhi AI Terminal", "bold", "cyan")
        # Header and bottom boxes
        top_bar = "┌" + ("─" * (max(2, cols - 2))) + "┐"
        title_line = "│" + title.center(max(2, cols - 2)) + "│"
        sep_line = "├" + ("─" * (max(2, cols - 2))) + "┤"
        bottom_bar = "└" + ("─" * (max(2, cols - 2))) + "┘"

        # Number of lines available in the content area (minus 4 lines in the upper and lower boxes)
        body_rows = max(1, usable_rows - 4)
        body = []
        for i in range(body_rows):
            text = lines[i] if i < len(lines) else ""
            text = style(text, "green") if i == 0 else text
            body.append("│" + text.ljust(max(2, cols - 2))[: max(2, cols - 2)] + "│")

        # Save cursor position
        sys.stdout.write("\x1b7")

        # Before drawing, completely clear the area that may remain in the previous frame to avoid visual "two layers"
        total_rows = 4 + body_rows  # Three lines in the top box + one line in the bottom box + number of text lines
        rows_to_clear = max(self._last_drawn_rows, total_rows)
        for i in range(rows_to_clear):
            self._goto(1 + i, 1)
            sys.stdout.write("\x1b[2K")

        # Draw the head
        self._goto(1, 1)
        sys.stdout.write("\x1b[2K" + top_bar[:cols])
        self._goto(2, 1)
        sys.stdout.write("\x1b[2K" + title_line[:cols])
        self._goto(3, 1)
        sys.stdout.write("\x1b[2K" + sep_line[:cols])

        # Draw the subject
        for idx in range(body_rows):
            self._goto(4 + idx, 1)
            sys.stdout.write("\x1b[2K")
            sys.stdout.write(body[idx][:cols])

        # bottom box
        self._goto(4 + body_rows, 1)
        sys.stdout.write("\x1b[2K" + bottom_bar[:cols])

        # Restore cursor position
        sys.stdout.write("\x1b8")
        sys.stdout.flush()

        # Record the height of this drawing
        self._last_drawn_rows = total_rows

    def _clear_input_area(self):
        if not self._use_ansi:
            return
        cols, rows = self._term_size()
        separator_row = max(1, rows - self._input_area_lines + 1)
        first_input_row = min(rows, separator_row + 1)
        second_input_row = min(rows, separator_row + 2)
        # Clear the separator line and the two input lines in order to avoid echo residue of Chinese wide characters.
        for r in [separator_row, first_input_row, second_input_row]:
            self._goto(r, 1)
            sys.stdout.write("\x1b[2K")
        sys.stdout.flush()

    async def _render_input_area(self):
        if not self._use_ansi:
            return
        cols, rows = self._term_size()
        separator_row = max(1, rows - self._input_area_lines + 1)
        first_input_row = min(rows, separator_row + 1)
        second_input_row = min(rows, separator_row + 2)

        # save cursor
        sys.stdout.write("\x1b7")
        # divider
        self._goto(separator_row, 1)
        sys.stdout.write("\x1b[2K")
        sys.stdout.write("═" * max(1, cols))

        # Enter prompt line (clear and write prompt)
        self._goto(first_input_row, 1)
        sys.stdout.write("\x1b[2K")
        prompt = "enter:" if not self._use_ansi else "\x1b[1m\x1b[36mInput:\x1b[0m"
        sys.stdout.write(prompt)

        # Reserve a line for overflow cleaning
        self._goto(second_input_row, 1)
        sys.stdout.write("\x1b[2K")
        sys.stdout.flush()

        # Restore the cursor to its original position, and then move the cursor to the input position for input use
        sys.stdout.write("\x1b8")
        self._goto(first_input_row, 1)
        sys.stdout.write(prompt)
        sys.stdout.flush()

    async def toggle_mode(self):
        """Mode switch in CLI mode (no operation)"""
        self.logger.debug("Mode switching is not supported in CLI mode")

    async def toggle_window_visibility(self):
        """Window switching in CLI mode (no operation)"""
        self.logger.debug("Window switching is not supported in CLI mode")
