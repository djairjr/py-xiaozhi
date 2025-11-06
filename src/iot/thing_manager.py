import asyncio
import json
from typing import Any, Dict, Optional, Tuple

from src.iot.thing import Thing
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class ThingManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThingManager()
        return cls._instance

    def __init__(self):
        self.things = []
        self.last_states = {}  # Add a state cache dictionary to store the last state

    async def initialize_iot_devices(self, config):
        """Initialize the IoT device.

        Note: The countdown timer functionality has been migrated to the MCP tool, providing better AI integration and status feedback."""
        from src.iot.things.lamp import Lamp

        # Add device
        self.add_thing(Lamp())

    def add_thing(self, thing: Thing) -> None:
        self.things.append(thing)

    async def get_descriptors_json(self) -> str:
        """Get descriptors JSON for all devices."""
        # Since get_descriptor_json() is a synchronous method (returns static data),
        # Just keep the synchronous call simple here
        descriptors = [thing.get_descriptor_json() for thing in self.things]
        return json.dumps(descriptors)

    async def get_states_json(self, delta=False) -> Tuple[bool, str]:
        """Get the status JSON of all devices.

        Args:
            delta: Whether to return only the changed part, True means only the changed part is returned

        Returns:
            Tuple[bool, str]: Returns a Boolean value and JSON string indicating whether there is a status change"""
        if not delta:
            self.last_states.clear()

        changed = False

        tasks = [thing.get_state_json() for thing in self.things]
        states_results = await asyncio.gather(*tasks)

        states = []
        for i, thing in enumerate(self.things):
            state_json = states_results[i]

            if delta:
                # Check if status changes
                is_same = (
                    thing.name in self.last_states
                    and self.last_states[thing.name] == state_json
                )
                if is_same:
                    continue
                changed = True
                self.last_states[thing.name] = state_json

            # Check if state_json is already a dictionary object
            if isinstance(state_json, dict):
                states.append(state_json)
            else:
                states.append(json.loads(state_json))  # Convert JSON string to dictionary

        return changed, json.dumps(states)

    async def get_states_json_str(self) -> str:
        """For compatibility with old code, the original method name and return value type are retained."""
        _, json_str = await self.get_states_json(delta=False)
        return json_str

    async def invoke(self, command: Dict) -> Optional[Any]:
        """Call device methods.

        Args:
            command: a command dictionary containing information such as name and method

        Returns:
            Optional[Any]: If the device is found and the call is successful, return the call result; otherwise throw an exception"""
        thing_name = command.get("name")
        for thing in self.things:
            if thing.name == thing_name:
                return await thing.invoke(command)

        # Record error log
        logger.error(f"Device does not exist: {thing_name}")
        raise ValueError(f"Device does not exist: {thing_name}")
