"""Music player singleton implementation.

Provides a music player in singleton mode, which is initialized during registration and supports asynchronous operations."""

import asyncio
import shutil
import tempfile
import time
from pathlib import Path
from typing import List, Optional, Tuple

import pygame
import requests

from src.constants.constants import AudioConfig
from src.utils.logging_config import get_logger
from src.utils.resource_finder import get_user_cache_dir

# Try importing the music metadata database
try:
    from mutagen import File as MutagenFile
    from mutagen.id3 import ID3NoHeaderError

    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

logger = get_logger(__name__)


class MusicMetadata:
    """Music metadata class."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.filename = file_path.name
        self.file_id = file_path.stem  # Remove the extension from the file name, which is the song ID
        self.file_size = file_path.stat().st_size

        # Metadata extracted from files
        self.title = None
        self.artist = None
        self.album = None
        self.duration = None  # seconds

    def extract_metadata(self) -> bool:
        """Extract music file metadata."""
        if not MUTAGEN_AVAILABLE:
            return False

        try:
            audio_file = MutagenFile(self.file_path)
            if audio_file is None:
                return False

            # Basic information
            if hasattr(audio_file, "info"):
                self.duration = getattr(audio_file.info, "length", None)

            # ID3 tag information
            tags = audio_file.tags if audio_file.tags else {}

            # title
            self.title = self._get_tag_value(tags, ["TIT2", "TITLE", "\xa9nam"])

            # artist
            self.artist = self._get_tag_value(tags, ["TPE1", "ARTIST", "\xa9ART"])

            # album
            self.album = self._get_tag_value(tags, ["TALB", "ALBUM", "\xa9alb"])

            return True

        except ID3NoHeaderError:
            # No ID3 tag, not an error
            return True
        except Exception as e:
            logger.debug(f"Failed to extract metadata {self.filename}: {e}")
            return False

    def _get_tag_value(self, tags: dict, tag_names: List[str]) -> Optional[str]:
        """Get values ​​from multiple possible tag names."""
        for tag_name in tag_names:
            if tag_name in tags:
                value = tags[tag_name]
                if isinstance(value, list) and value:
                    return str(value[0])
                elif value:
                    return str(value)
        return None

    def format_duration(self) -> str:
        """Format playback duration."""
        if self.duration is None:
            return "unknown"

        minutes = int(self.duration) // 60
        seconds = int(self.duration) % 60
        return f"{minutes:02d}:{seconds:02d}"


class MusicPlayer:
    """Music Player - Designed for IoT Devices

    Only retain core functions: search, play, pause, stop, jump"""

    def __init__(self):
        # Optimize pygame mixer initialization according to server type
        self._init_pygame_mixer()

        # Core play status
        self.current_song = ""
        self.current_url = ""
        self.song_id = ""
        self.total_duration = 0
        self.is_playing = False
        self.paused = False
        self.current_position = 0
        self.start_play_time = 0

        # Lyrics related
        self.lyrics = []  # Lyrics list in the format [(time, text), ...]
        self.current_lyric_index = -1  # Current lyrics index

        # Cache Directory Settings - Use user cache directory to ensure it is writable
        user_cache_dir = get_user_cache_dir()
        self.cache_dir = user_cache_dir / "music"
        self.temp_cache_dir = self.cache_dir / "temp"
        self._init_cache_dirs()

        # API configuration
        self.config = {
            "SEARCH_URL": "http://search.kuwo.cn/r.s",
            "PLAY_URL": "http://api.xiaodaokg.com/kuwo.php",
            "LYRIC_URL": "https://api.xiaodaokg.com/kw/kwlyric.php",
            "HEADERS": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36"
                ),
                "Accept": "*/*",
                "Connection": "keep-alive",
            },
        }

        # Clear temporary cache
        self._clean_temp_cache()

        # Get application instance
        self.app = None
        self._initialize_app_reference()

        # Local playlist cache
        self._local_playlist = None
        self._last_scan_time = 0

        logger.info("Music player singleton initialization completed")

    def _init_pygame_mixer(self):
        """Optimize pygame mixer initialization based on server type."""
        try:

            # Pre-initialize mixer to set buffer
            pygame.mixer.pre_init(
                frequency=AudioConfig.OUTPUT_SAMPLE_RATE,
                size=-16,  # 16-bit signed
                channels=AudioConfig.CHANNELS,
                buffer=1024,
            )

            # Formal initialization
            pygame.mixer.init()

            logger.info(
                f"pygame mixer initialization completed - sampling rate: {AudioConfig.OUTPUT_SAMPLE_RATE}Hz"
            )

        except Exception as e:
            logger.warning(f"Optimizing pygame initialization failed, using default configuration: {e}")
            # Fall back to default configuration
            pygame.mixer.init(
                frequency=AudioConfig.OUTPUT_SAMPLE_RATE, channels=AudioConfig.CHANNELS
            )

    def _initialize_app_reference(self):
        """Initialize application reference."""
        try:
            from src.application import Application

            self.app = Application.get_instance()
        except Exception as e:
            logger.warning(f"Failed to obtain Application instance: {e}")
            self.app = None

    def _init_cache_dirs(self):
        """Initialize the cache directory."""
        try:
            # Create main cache directory
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            # Create temporary cache directory
            self.temp_cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Music cache directory initialization completed: {self.cache_dir}")
        except Exception as e:
            logger.error(f"Failed to create cache directory: {e}")
            # Fall back to the system temporary directory
            self.cache_dir = Path(tempfile.gettempdir()) / "xiaozhi_music_cache"
            self.temp_cache_dir = self.cache_dir / "temp"
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.temp_cache_dir.mkdir(parents=True, exist_ok=True)

    def _clean_temp_cache(self):
        """Clean temporary cache files."""
        try:
            # Clear all files in the temporary cache directory
            for file_path in self.temp_cache_dir.glob("*"):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        logger.debug(f"Deleted temporary cache file: {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to delete temporary cache file: {file_path.name}, {e}")

            logger.info("Temporary music cache cleanup completed")
        except Exception as e:
            logger.error(f"Failed to clear temporary cache directory: {e}")

    def _scan_local_music(self, force_refresh: bool = False) -> List[MusicMetadata]:
        """Scan the local music cache and return to the playlist."""
        current_time = time.time()

        # If there is no forced refresh and the cache has not expired (5 minutes), return to the cache directly.
        if (
            not force_refresh
            and self._local_playlist is not None
            and (current_time - self._last_scan_time) < 300
        ):
            return self._local_playlist

        playlist = []

        if not self.cache_dir.exists():
            logger.warning(f"The cache directory does not exist: {self.cache_dir}")
            return playlist

        # Find all music files
        music_files = []
        for pattern in ["*.mp3", "*.m4a", "*.flac", "*.wav", "*.ogg"]:
            music_files.extend(self.cache_dir.glob(pattern))

        logger.debug(f"{len(music_files)} music files found")

        # Scan every file
        for file_path in music_files:
            try:
                metadata = MusicMetadata(file_path)

                # Try to extract metadata
                if MUTAGEN_AVAILABLE:
                    metadata.extract_metadata()

                playlist.append(metadata)

            except Exception as e:
                logger.debug(f"Failed to process music file {file_path.name}: {e}")

        # Sort by artist and title
        playlist.sort(key=lambda x: (x.artist or "Unknown", x.title or x.filename))

        # Update cache
        self._local_playlist = playlist
        self._last_scan_time = current_time

        logger.info(f"Scanning completed, {len(playlist)} local music found")
        return playlist

    async def get_local_playlist(self, force_refresh: bool = False) -> dict:
        """Get local music playlists."""
        try:
            playlist = self._scan_local_music(force_refresh)

            if not playlist:
                return {
                    "status": "info",
                    "message": "No music files in local cache",
                    "playlist": [],
                    "total_count": 0,
                }

            # Format the playlist in a concise format that is easy for AI to read
            formatted_playlist = []
            for metadata in playlist:
                title = metadata.title or "Unknown title"
                artist = metadata.artist or "unknown artist"
                song_info = f"{title} - {artist}"
                formatted_playlist.append(song_info)

            return {
                "status": "success",
                "message": f"Found {len(playlist)} local music",
                "playlist": formatted_playlist,
                "total_count": len(playlist),
            }

        except Exception as e:
            logger.error(f"Failed to obtain local playlist: {e}")
            return {
                "status": "error",
                "message": f"Failed to obtain local playlist: {str(e)}",
                "playlist": [],
                "total_count": 0,
            }

    async def search_local_music(self, query: str) -> dict:
        """Search local music."""
        try:
            playlist = self._scan_local_music()

            if not playlist:
                return {
                    "status": "info",
                    "message": "No music files in local cache",
                    "results": [],
                    "found_count": 0,
                }

            query = query.lower()
            results = []

            for metadata in playlist:
                # Search within title, artist, filename
                searchable_text = " ".join(
                    filter(
                        None,
                        [
                            metadata.title,
                            metadata.artist,
                            metadata.album,
                            metadata.filename,
                        ],
                    )
                ).lower()

                if query in searchable_text:
                    title = metadata.title or "Unknown title"
                    artist = metadata.artist or "unknown artist"
                    song_info = f"{title} - {artist}"
                    results.append(
                        {
                            "song_info": song_info,
                            "file_id": metadata.file_id,
                            "duration": metadata.format_duration(),
                        }
                    )

            return {
                "status": "success",
                "message": f"Found {len(results)} matching songs in local music",
                "results": results,
                "found_count": len(results),
            }

        except Exception as e:
            logger.error(f"Failed to search local music: {e}")
            return {
                "status": "error",
                "message": f"Search failed: {str(e)}",
                "results": [],
                "found_count": 0,
            }

    async def play_local_song_by_id(self, file_id: str) -> dict:
        """Play local songs based on file ID."""
        try:
            # Build file path
            file_path = self.cache_dir / f"{file_id}.mp3"

            if not file_path.exists():
                # Try another format
                for ext in [".m4a", ".flac", ".wav", ".ogg"]:
                    alt_path = self.cache_dir / f"{file_id}{ext}"
                    if alt_path.exists():
                        file_path = alt_path
                        break
                else:
                    return {"status": "error", "message": f"Local file does not exist: {file_id}"}

            # Get song information
            metadata = MusicMetadata(file_path)
            if MUTAGEN_AVAILABLE:
                metadata.extract_metadata()

            # Stop current playback
            if self.is_playing:
                pygame.mixer.music.stop()

            # Load and play
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()

            # Update playback status
            title = metadata.title or "Unknown title"
            artist = metadata.artist or "unknown artist"
            self.current_song = f"{title} - {artist}"
            self.song_id = file_id
            self.total_duration = metadata.duration or 0
            self.current_url = str(file_path)  # local file path
            self.is_playing = True
            self.paused = False
            self.current_position = 0
            self.start_play_time = time.time()
            self.current_lyric_index = -1
            self.lyrics = []  # Local files do not support lyrics yet

            logger.info(f"Start playing local music: {self.current_song}")

            # Update UI
            if self.app and hasattr(self.app, "set_chat_message"):
                await self._safe_update_ui(f"Playing local music: {self.current_song}")

            return {
                "status": "success",
                "message": f"Playing local music: {self.current_song}",
            }

        except Exception as e:
            logger.error(f"Failed to play local music: {e}")
            return {"status": "error", "message": f"Playback failed: {str(e)}"}

    # Property getter method
    async def get_current_song(self):
        return self.current_song

    async def get_is_playing(self):
        return self.is_playing

    async def get_paused(self):
        return self.paused

    async def get_duration(self):
        return self.total_duration

    async def get_position(self):
        if not self.is_playing or self.paused:
            return self.current_position

        current_pos = min(self.total_duration, time.time() - self.start_play_time)

        # Check if playback is complete
        if current_pos >= self.total_duration and self.total_duration > 0:
            await self._handle_playback_finished()

        return current_pos

    async def get_progress(self):
        """Get the playback progress percentage."""
        if self.total_duration <= 0:
            return 0
        position = await self.get_position()
        return round(position * 100 / self.total_duration, 1)

    async def _handle_playback_finished(self):
        """Processing and playback completed."""
        if self.is_playing:
            logger.info(f"Song playback completed: {self.current_song}")
            pygame.mixer.music.stop()
            self.is_playing = False
            self.paused = False
            self.current_position = self.total_duration

            # Update UI to show completion status
            if self.app and hasattr(self.app, "set_chat_message"):
                dur_str = self._format_time(self.total_duration)
                await self._safe_update_ui(f"Playback completed: {self.current_song} [{dur_str}]")

    # core method
    async def search_and_play(self, song_name: str) -> dict:
        """Search and play songs."""
        try:
            # Search for songs
            song_id, url = await self._search_song(song_name)
            if not song_id or not url:
                return {"status": "error", "message": f"Song not found: {song_name}"}

            # play song
            success = await self._play_url(url)
            if success:
                return {
                    "status": "success",
                    "message": f"Now playing: {self.current_song}",
                }
            else:
                return {"status": "error", "message": "Play failed"}

        except Exception as e:
            logger.error(f"Search playback failed: {e}")
            return {"status": "error", "message": f"Operation failed: {str(e)}"}

    async def play_pause(self) -> dict:
        """Play/pause switch."""
        try:
            if not self.is_playing and self.current_url:
                # Replay
                success = await self._play_url(self.current_url)
                return {
                    "status": "success" if success else "error",
                    "message": (
                        f"Start playing: {self.current_song}" if success else "Play failed"
                    ),
                }

            elif self.is_playing and self.paused:
                # Resume playback
                pygame.mixer.music.unpause()
                self.paused = False
                self.start_play_time = time.time() - self.current_position

                # Update UI
                if self.app and hasattr(self.app, "set_chat_message"):
                    await self._safe_update_ui(f"Continue playing: {self.current_song}")

                return {
                    "status": "success",
                    "message": f"Continue playing: {self.current_song}",
                }

            elif self.is_playing and not self.paused:
                # Pause playback
                pygame.mixer.music.pause()
                self.paused = True
                self.current_position = time.time() - self.start_play_time

                # Update UI
                if self.app and hasattr(self.app, "set_chat_message"):
                    pos_str = self._format_time(self.current_position)
                    dur_str = self._format_time(self.total_duration)
                    await self._safe_update_ui(
                        f"Paused: {self.current_song} [{pos_str}/{dur_str}]"
                    )

                return {"status": "success", "message": f"Paused: {self.current_song}"}

            else:
                return {"status": "error", "message": "No songs available to play"}

        except Exception as e:
            logger.error(f"Playback pause operation failed: {e}")
            return {"status": "error", "message": f"Operation failed: {str(e)}"}

    async def stop(self) -> dict:
        """Stop playing."""
        try:
            if not self.is_playing:
                return {"status": "info", "message": "No songs playing"}

            pygame.mixer.music.stop()
            current_song = self.current_song
            self.is_playing = False
            self.paused = False
            self.current_position = 0

            # Update UI
            if self.app and hasattr(self.app, "set_chat_message"):
                await self._safe_update_ui(f"Stopped: {current_song}")

            return {"status": "success", "message": f"Stopped: {current_song}"}

        except Exception as e:
            logger.error(f"Failed to stop playback: {e}")
            return {"status": "error", "message": f"Stop failed: {str(e)}"}

    async def seek(self, position: float) -> dict:
        """Jump to the specified location."""
        try:
            if not self.is_playing:
                return {"status": "error", "message": "No songs playing"}

            position = max(0, min(position, self.total_duration))
            self.current_position = position
            self.start_play_time = time.time() - position

            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(position)

            if self.paused:
                pygame.mixer.music.pause()

            # Update UI
            pos_str = self._format_time(position)
            dur_str = self._format_time(self.total_duration)
            if self.app and hasattr(self.app, "set_chat_message"):
                await self._safe_update_ui(f"Jumped to: {pos_str}/{dur_str}")

            return {"status": "success", "message": f"Jumped to: {position:.1f} seconds"}

        except Exception as e:
            logger.error(f"Jump failed: {e}")
            return {"status": "error", "message": f"Jump failed: {str(e)}"}

    async def get_lyrics(self) -> dict:
        """Get the lyrics of the current song."""
        if not self.lyrics:
            return {"status": "info", "message": "The current song has no lyrics", "lyrics": []}

        # Extract lyrics text and convert to list
        lyrics_text = []
        for time_sec, text in self.lyrics:
            time_str = self._format_time(time_sec)
            lyrics_text.append(f"[{time_str}] {text}")

        return {
            "status": "success",
            "message": f"Get {len(self.lyrics)} lines of lyrics",
            "lyrics": lyrics_text,
        }

    async def get_status(self) -> dict:
        """Get player status."""
        position = await self.get_position()
        progress = await self.get_progress()

        return {
            "status": "success",
            "current_song": self.current_song,
            "is_playing": self.is_playing,
            "paused": self.paused,
            "duration": self.total_duration,
            "position": position,
            "progress": progress,
            "has_lyrics": len(self.lyrics) > 0,
        }

    # internal method
    async def _search_song(self, song_name: str) -> Tuple[str, str]:
        """Search songs to get ID and URL."""
        try:
            # Build search parameters
            params = {
                "all": song_name,
                "ft": "music",
                "newsearch": "1",
                "alflac": "1",
                "itemset": "web_2013",
                "client": "kt",
                "cluster": "0",
                "pn": "0",
                "rn": "1",
                "vermerge": "1",
                "rformat": "json",
                "encoding": "utf8",
                "show_copyright_off": "1",
                "pcmp4": "1",
                "ver": "mbox",
                "vipver": "MUSIC_8.7.6.0.BCS31",
                "plat": "pc",
                "devid": "0",
            }

            # Search for songs
            response = await asyncio.to_thread(
                requests.get,
                self.config["SEARCH_URL"],
                params=params,
                headers=self.config["HEADERS"],
                timeout=10,
            )
            response.raise_for_status()

            # Parse response
            text = response.text.replace("'", '"')

            #Extract song ID
            song_id = self._extract_value(text, '"(text, '"DC_TARGETID":"', '"')
            if not song_id:
                return "", ""# Extract song information
            title = self._extract_value(text, '"act_value(text, '"NAME":"', '"') or song_name
            artist = self._extract_value(text, '"ARTIST":"', '"')
            album = self._extract_value(text, '"ALBUM":"', '"')
            duration_str = self._extract_value(text, '"DURATION":"', '"')

            if duration_str:
                try:
                    self.total_duration = int(duration_str)
                except ValueError:
                    self.total_duration = 0

            # Set display name
            display_name = title
            if artist:
                display_name = f"_name = f"{title} - {artist}"
                if album:
                    display_name += f" ({album})"self.current_song = display_name
            self.song_id = song_id

            # Get playback URL
            play_url = f"_url = f"{self.config['PLAY_URL']}?ID={song_id}"
            url_response = await asyncio.to_thread(
                requests.get, play_url, headers=self.config["HEADERS"], timeout=10
            )
            url_response.raise_for_status()

            play_url_text = url_response.text.strip()
            if play_url_text and play_url_text.startswith("http"):
                # Get lyrics
                await self._fetch_lyrics(song_id)
                return song_id, play_url_text

            return song_id,"_id, ""

        except Exception as e:
            logger.error(f"搜索歌曲失败: {e}")
            return "", ""

    async def _play_url(self, url: str) -> bool:
        """
        播放指定URL.
        """try:
            # Stop current playback
            if self.is_playing:
                pygame.mixer.music.stop()

            # Check cache or download
            file_path = await self._get_or_download_file(url)
            if not file_path:
                return False

            # Load and play
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()

            self.current_url = url
            self.is_playing = True
            self.paused = False
            self.current_position = 0
            self.start_play_time = time.time()
            self.current_lyric_index = -1 # Reset lyrics index

            logger.info(f"1  # Reset lyrics index

            logger.info(f"开始播放: {self.current_song}")

            # Update UI
            if self.app and hasattr(self.app,"pp, "set_chat_message"):
                await self._safe_update_ui(f"正在播放: {self.current_song}")

            # Start the lyrics update task
            asyncio.create_task(self._lyrics_update_task())

            return True

        except Exception as e:
            logger.error(f"     logger.error(f"播放失败: {e}")
            return False

    async def _get_or_download_file(self, url: str) -> Optional[Path]:
        """获取或下载文件.

        先检查缓存，如果缓存中没有则下载
        """try:
            # Use song ID as cache file name
            cache_filename = f"che_filename = f"{self.song_id}.mp3"cache_path = self.cache_dir/cache_filename

            # Check if cache exists
            if cache_path.exists():
                logger.info(f"ogger.info(f"使用缓存: {cache_path}")
                return cache_path

            # The cache does not exist and needs to be downloaded.
            return await self._download_file(url, cache_filename)

        except Exception as e:
            logger.error(f"ception as e:
            logger.error(f"获取文件失败: {e}")
            return None

    async def _download_file(self, url: str, filename: str) -> Optional[Path]:
        """下载文件到缓存目录.

        先下载到临时目录，下载完成后移动到正式缓存目录
        """temp_path = None
        try:
            #Create temporary file path
            temp_path = self.temp_cache_dir/f"emp_cache_dir / f"temp_{int(time.time())}_{filename}"# Asynchronous download
            response = await asyncio.to_thread(
                requests.get,
                url,
                headers=self.config["ers=self.config["HEADERS"],
                stream=True,
                timeout=30,
            )
            response.raise_for_status()

            #Write to temporary file
            with open(temp_path,"open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # After the download is completed, move to the official cache directory
            cache_path = self.cache_dir/filename
            shutil.move(str(temp_path), str(cache_path))

            logger.info(f"r(cache_path))

            logger.info(f"音乐下载完成并缓存: {cache_path}")
            return cache_path

        except Exception as e:
            logger.error(f"下载失败: {e}")
            # Clean up temporary files
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                    logger.debug(f"logger.debug(f"已清理临时下载文件: {temp_path}")
                except Exception:
                    pass
            return None

    async def _fetch_lyrics(self, song_id: str):
        """
        获取歌词.
        """try:
            # reset lyrics
            self.lyrics = []

            # Construct lyrics API request
            lyric_url = self.config.get("ric_url = self.config.get("LYRIC_URL")
            lyric_api_url = f"{lyric_url}?id={song_id}"
            logger.info(f"获取歌词URL: {lyric_api_url}")

            response = await asyncio.to_thread(
                requests.get, lyric_api_url, headers=self.config["HEADERS"], timeout=10
            )
            response.raise_for_status()

            # Parse JSON
            data = response.json()

            # Parse lyrics
            if (
                data.get("  data.get("code") == 200
                and data.get("data")
                and data["data"].get("content")
            ):
                lrc_content = data["data"]["content"]

                # Parse LRC format lyrics
                lines = lrc_content.split("ontent.split("\n")
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    # Match time tag format [mm:ss.xx]
                    import re

                    time_match = re.match(r" = re.match(r"\[(\d{2}):(\d{2})\.(\d{2})\](.+)", line)
                    if time_match:
                        minutes = int(time_match.group(1))
                        seconds = int(time_match.group(2))
                        centiseconds = int(time_match.group(3))
                        text = time_match.group(4).strip()

                        # Convert to total seconds
                        time_sec = minutes * 60 + seconds + centiseconds / 100.0

                        # Skip empty lyrics and meta information lyrics
                        if (
                            text
                            and not text.startswith("                           and not text.startswith("作词")
                            and not text.startswith("作曲")
                            and not text.startswith("编曲")
                            and not text.startswith("ti:")
                            and not text.startswith("ar:")
                            and not text.startswith("al:")
                            and not text.startswith("by:")
                            and not text.startswith("offset:")
                        ):
                            self.lyrics.append((time_sec, text))

                logger.info(f"成功获取歌词，共 {len(self.lyrics)} 行")
            else:
                logger.warning(f"未获取到歌词或歌词格式错误: {data.get('msg', '')}")

        except Exception as e:
            logger.error(f"获取歌词失败: {e}")

    async def _lyrics_update_task(self):
        """
        歌词更新任务.
        """if not self.lyrics:
            return

        try:
            while self.is_playing:
                if self.paused:
                    await asyncio.sleep(0.5)
                    continue

                current_time = time.time() - self.start_play_time

                # Check if playback is complete
                if current_time >= self.total_duration:
                    await self._handle_playback_finished()
                    break

                # Find lyrics corresponding to the current time
                current_index = self._find_current_lyric_index(current_time)

                # If the lyrics index changes, update the display
                if current_index != self.current_lyric_index:
                    await self._display_current_lyric(current_index)

                await asyncio.sleep(0.2)
        except Exception as e:
            logger.error(f"     await asyncio.sleep(0.2)
        except Exception as e:
            logger.error(f"歌词更新任务异常: {e}")

    def _find_current_lyric_index(self, current_time: float) -> int:
        """
        查找当前时间对应的歌词索引.
        """# Find the next lyrics
        next_lyric_index = None
        for i, (time_sec, _) in enumerate(self.lyrics):
            # Add a small offset (0.5 seconds) to make the lyrics display more accurate
            if time_sec > current_time - 0.5:
                next_lyric_index = i
                break

        # Determine the current lyrics index
        if next_lyric_index is not None and next_lyric_index > 0:
            # If the next lyric is found, the current lyric is its previous sentence
            return next_lyric_index - 1
        elif next_lyric_index is None and self.lyrics:
            # If the next sentence is not found, it means we have reached the last sentence.
            return len(self.lyrics) - 1
        else:
            # Other situations (such as just starting playback)
            return 0

    async def _display_current_lyric(self, current_index: int):"sentence.
            return len(self.lyrics) - 1
        else:
            # Other situations (such as playback just started)
            return 0

    async def _display_current_lyric(self, current_index: int):
        """
        显示当前歌词.
        """self.current_lyric_index = current_index

        if current_index < len(self.lyrics):
            time_sec, text = self.lyrics[current_index]

            # Add time and progress information before lyrics
            position_str = self._format_time(time.time() - self.start_play_time)
            duration_str = self._format_time(self.total_duration)
            display_text = f"ion)
            display_text = f"[{position_str}/{duration_str}] {text}"# Update UI
            if self.app and hasattr(self.app,"pp, "set_chat_message"):
                await self._safe_update_ui(display_text)
                logger.debug(f"显示歌词: {text}")

    def _extract_value(self, text: str, start_marker: str, end_marker: str) -> str:
        """
        从文本中提取值.
        """
        start_pos = text.find(start_marker)
        if start_pos == -1:
            return ""

        start_pos += len(start_marker)
        end_pos = text.find(end_marker, start_pos)

        if end_pos == -1:
            return ""

        return text[start_pos:end_pos]

    def _format_time(self, seconds: float) -> str:
        """
        将秒数格式化为 mm:ss 格式.
        """
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes:02d}:{seconds:02d}"

    async def _safe_update_ui(self, message: str):
        """
        安全地更新UI.
        """
        if not self.app or not hasattr(self.app, "set_chat_message"):
            return

        try:
            self.app.set_chat_message("assistant", message)
        except Exception as e:
            logger.error(f"更新UI失败: {e}")

    def __del__(self):
        """
        清理资源.
        """try:
            # If the program exits normally, clean the temporary cache once more
            self._clean_temp_cache()
        exceptException:
            # Ignore errors because there may be various exceptions during the object destruction phase
            pass


#Global music player instance
_music_player_instance = None


def get_music_player_instance() -> MusicPlayer:"      pass


# Global music player instance
_music_player_instance = None


def get_music_player_instance() -> MusicPlayer:
    """
    获取音乐播放器单例.
    """
    global _music_player_instance
    if _music_player_instance is None:
        _music_player_instance = MusicPlayer()
        logger.info("[MusicPlayer] 创建音乐播放器单例实例")
    return _music_player_instance
