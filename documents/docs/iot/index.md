# IoT Device Development Guide

## Overview

The py-xiaozhi project adopts an IoT device architecture based on Thing Pattern to provide a unified device abstraction and management interface. All devices inherit from the Thing base class and are centrally managed through ThingManager. The architecture supports asynchronous operations, type-safe parameter handling, and state management.

**Important note**: The current project is migrating from the IoT device mode to the MCP (Model Context Protocol) tool mode, and some device functions have been migrated to the MCP tool system.

## Core architecture

### Directory structure

```
src/iot/
├── thing.py # Core base class and tool class
│ ├── Thing # Device abstract base class
│ ├── Property # Equipment property class
│ ├── Method # Device method class
│ ├── Parameter # Method parameter class
│ └── ValueType # Parameter type enumeration
├── thing_manager.py # Device Manager
│ └── ThingManager # Singleton device manager
└── things/ # Device implementation
├── lamp.py # lighting equipment
├── speaker.py # Audio equipment
├── music_player.py # Music player
├── countdown_timer.py # Countdown timer
└── CameraVL/ # Camera equipment
        ├── Camera.py
        └── VL.py
```

### Core components

#### 1. Thing base class

Thing is the abstract base class for all IoT devices, providing unified interface specifications:

```python
from src.iot.thing import Thing, Parameter, ValueType

class Thing:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.properties = {}
        self.methods = {}
    
    def add_property(self, name: str, description: str, getter: Callable)
    def add_method(self, name: str, description: str, parameters: List[Parameter], callback: Callable)
    async def get_descriptor_json(self) -> str
    async def get_state_json(self) -> str
    async def invoke(self, command: dict) -> dict
```

**Key Requirements:**

- All property getter functions must be asynchronous (`async def`)
- All method callback functions must be asynchronous
- Device name must be globally unique

#### 2. Property attribute system

Property is used to define the readable state of the device and supports automatic type inference:

```python
class Property:
    def __init__(self, name: str, description: str, getter: Callable):
# Force getter to be an asynchronous function
        if not inspect.iscoroutinefunction(getter):
            raise TypeError(f"Property getter for '{name}' must be an async function.")
```

**Supported attribute types:**

- `boolean`: Boolean value
- `number`: integer
- `string`: string
- `float`: floating point number
- `array`: array
- `object`: object

#### 3. Method method system

Method is used to define the executable operation of the device:

```python
class Method:
    def __init__(self, name: str, description: str, parameters: List[Parameter], callback: Callable):
# Force the callback function to be an asynchronous function
        if not inspect.iscoroutinefunction(callback):
            raise TypeError(f"Method callback for '{name}' must be an async function.")
```

#### 4. Parameter parameter system

Parameter defines the parameter specification of the method:

```python
class Parameter:
    def __init__(self, name: str, description: str, type_: str, required: bool = True):
        self.name = name
        self.description = description
        self.type = type_
        self.required = required
    
    def get_value(self):
        return self.value
```

**Supported parameter types:**

- `ValueType.BOOLEAN`: Boolean value
- `ValueType.NUMBER`: integer
- `ValueType.STRING`: string
- `ValueType.FLOAT`: floating point number
- `ValueType.ARRAY`: array
- `ValueType.OBJECT`: object

#### 5. ThingManager manager

ThingManager adopts singleton mode and is responsible for device registration, status management and method invocation:

```python
from src.iot.thing_manager import ThingManager

class ThingManager:
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ThingManager()
        return cls._instance
    
    def add_thing(self, thing: Thing)
    async def get_states_json(self, delta: bool = False) -> Tuple[bool, str]
    async def get_descriptors_json(self) -> str
    async def invoke(self, command: dict) -> dict
```

**Core features:**

- Device registration and management
- State caching and incremental updates
- Method call distribution
- Device description information query

## Device implementation mode

### 1. Basic equipment - Lamp

The simplest device implementation mode:

```python
import asyncio
from src.iot.thing import Thing

class Lamp(Thing):
    def __init__(self):
super().__init__("Lamp", "A test lamp")
        self.power = False
        
# Register property - getter must be an asynchronous function
self.add_property("power", "Whether the light is on", self.get_power)
        
#Registration method - callback must be an asynchronous function
self.add_method("TurnOn", "Turn on the light", [], self._turn_on)
self.add_method("TurnOff", "Turn off the light", [], self._turn_off)
    
    async def get_power(self):
        return self.power
    
    async def _turn_on(self, params):
        self.power = True
return {"status": "success", "message": "Light is on"}
    
    async def _turn_off(self, params):
        self.power = False
return {"status": "success", "message": "Light is off"}
```

### 2. Device with parameters - Speaker

Device implementation with parameter verification:

```python
import asyncio
from src.iot.thing import Thing, Parameter, ValueType
from src.utils.volume_controller import VolumeController

class Speaker(Thing):
    def __init__(self):
super().__init__("Speaker", "The speaker of the current AI robot")
        
#Initialize the volume controller
        self.volume_controller = None
        try:
            if VolumeController.check_dependencies():
                self.volume_controller = VolumeController()
                self.volume = self.volume_controller.get_volume()
            else:
                self.volume = 70
        except Exception:
            self.volume = 70
        
#Register attributes
self.add_property("volume", "Current volume value", self.get_volume)
        
# Register method with parameters
        self.add_method(
            "SetVolume",
"Set volume",
[Parameter("volume", "Integer between 0 and 100", ValueType.NUMBER, True)],
            self._set_volume,
        )
    
    async def get_volume(self):
        if self.volume_controller:
            try:
                self.volume = self.volume_controller.get_volume()
            except Exception:
                pass
        return self.volume
    
    async def _set_volume(self, params):
# Get the value from the Parameter object
        volume = params["volume"].get_value()
        
# Parameter validation
        if not (0 <= volume <= 100):
raise ValueError("Volume must be between 0-100")
        
        self.volume = volume
        try:
            if self.volume_controller:
# Asynchronously call system API
                await asyncio.to_thread(self.volume_controller.set_volume, volume)
return {"success": True, "message": f"The volume has been set to: {volume}"}
        except Exception as e:
return {"success": False, "message": f"Failed to set volume: {e}"}
```

### 3. Complex device - CountdownTimer

Device implementation of asynchronous task management:

```python
import asyncio
import json
from typing import Dict
from asyncio import Task
from src.iot.thing import Thing, Parameter
from src.iot.thing_manager import ThingManager

class CountdownTimer(Thing):
    def __init__(self):
super().__init__("CountdownTimer", "A countdown timer used to delay the execution of commands")
        
# Task management
        self._timers: Dict[int, Task] = {}
        self._next_timer_id = 0
        self._lock = asyncio.Lock()
        
#Registration method
        self.add_method(
            "StartCountdown",
"Start a countdown and execute the specified command after it ends",
            [
Parameter("command", "IoT command to be executed (JSON format string)", "string", True),
Parameter("delay", "Delay time (seconds), default is 5 seconds", "integer", False)
            ],
            self._start_countdown,
        )
        
        self.add_method(
            "CancelCountdown",
"Cancel the specified countdown",
[Parameter("timer_id", "Timer ID to be canceled", "integer", True)],
            self._cancel_countdown,
        )
    
    async def _start_countdown(self, params_dict):
# Process required parameters
        command_param = params_dict.get("command")
        command_str = command_param.get_value() if command_param else None
        
        if not command_str:
return {"status": "error", "message": "Missing 'command' parameter value"}
        
# Handle optional parameters
        delay_param = params_dict.get("delay")
        delay = (
            delay_param.get_value()
            if delay_param and delay_param.get_value() is not None
            else 5
        )
        
# Verify command format
        try:
            json.loads(command_str)
        except json.JSONDecodeError:
return {"status": "error", "message": "The command format is wrong and JSON cannot be parsed"}
        
# Create an asynchronous task
        async with self._lock:
            timer_id = self._next_timer_id
            self._next_timer_id += 1
            task = asyncio.create_task(
                self._delayed_execution(delay, timer_id, command_str)
            )
            self._timers[timer_id] = task
        
        return {
            "status": "success",
"message": f"Countdown {timer_id} has been started and will be executed in {delay} seconds",
            "timer_id": timer_id
        }
    
    async def _delayed_execution(self, delay: int, timer_id: int, command_str: str):
        try:
            await asyncio.sleep(delay)
#Execute command
            command_dict = json.loads(command_str)
            thing_manager = ThingManager.get_instance()
            result = await thing_manager.invoke(command_dict)
print(f"Countdown {timer_id} execution result: {result}")
        except asyncio.CancelledError:
print(f"Countdown {timer_id} is canceled")
        finally:
            async with self._lock:
                self._timers.pop(timer_id, None)
    
    async def _cancel_countdown(self, params_dict):
        timer_id_param = params_dict.get("timer_id")
        timer_id = timer_id_param.get_value() if timer_id_param else None
        
        if timer_id is None:
return {"status": "error", "message": "Missing 'timer_id' parameter value"}
        
        async with self._lock:
            if timer_id in self._timers:
                task = self._timers.pop(timer_id)
                task.cancel()
return {"status": "success", "message": f"Countdown {timer_id} has been canceled"}
            else:
return {"status": "error", "message": "Timer does not exist"}
```

### 4. Multi-threaded device - Camera

Device implementation integrating multi-threading and external services:

```python
import threading
import base64
import cv2
from src.iot.thing import Thing
from src.iot.things.CameraVL.VL import ImageAnalyzer

class Camera(Thing):
    def __init__(self):
super().__init__("Camera", "Camera Management")
        self.cap = None
        self.is_running = False
        self.camera_thread = None
        self.result = ""
        
#Initialize VL analyzer
        self.VL = ImageAnalyzer.get_instance()
        
#Register attributes
self.add_property("power", "Is the camera on?", self.get_power)
self.add_property("result", "Identify the content of the screen", self.get_result)
        
#Registration method
self.add_method("start_camera", "Open camera", [], self.start_camera)
self.add_method("stop_camera", "Turn off the camera", [], self.stop_camera)
self.add_method("capture_frame_to_base64", "Recognition screen", [], self.capture_frame_to_base64)
    
    async def get_power(self):
        return self.is_running
    
    async def get_result(self):
        return self.result
    
    async def start_camera(self, params):
        if self.camera_thread and self.camera_thread.is_alive():
return {"status": "info", "message": "Camera is running"}
        
        self.camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
        self.camera_thread.start()
return {"status": "success", "message": "Camera has been started"}
    
    async def stop_camera(self, params):
        self.is_running = False
        if self.camera_thread:
            self.camera_thread.join()
            self.camera_thread = None
return {"status": "success", "message": "Camera has stopped"}
    
    async def capture_frame_to_base64(self, params):
        if not self.cap or not self.cap.isOpened():
return {"status": "error", "message": "Camera is not turned on"}
        
        ret, frame = self.cap.read()
        if not ret:
return {"status": "error", "message": "Unable to read screen"}
        
# Convert to base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
# Use VL analyzer to identify the screen
        self.result = str(self.VL.analyze_image(frame_base64))
        
        return {"status": "success", "result": self.result}
    
    def _camera_loop(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return
        
        self.is_running = True
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.is_running = False
        
        self.cap.release()
        cv2.destroyAllWindows()
```

## Device registration and management

### 1. Device registration

Register the device when the application starts:

```python
from src.iot.thing_manager import ThingManager
from src.iot.things.lamp import Lamp
from src.iot.things.speaker import Speaker

def initialize_iot_devices():
# Get device manager instance
    manager = ThingManager.get_instance()
    
# Register device
    manager.add_thing(Lamp())
    manager.add_thing(Speaker())
    
print(f"{len(manager.things)} devices have been registered")
```

### 2. Equipment status query

```python
# Get all device status
changed, states = await manager.get_states_json(delta=False)
print(f"Device status: {states}")

# Get the changed status (incremental update)
changed, delta_states = await manager.get_states_json(delta=True)
if changed:
print(f"State change: {delta_states}")
```

### 3. Device method call

```python
# Call device method
command = {
    "name": "Lamp",
    "method": "TurnOn",
    "parameters": {}
}
result = await manager.invoke(command)
print(f"Execution result: {result}")

# Method call with parameters
command = {
    "name": "Speaker",
    "method": "SetVolume",
    "parameters": {"volume": 80}
}
result = await manager.invoke(command)
```

## Development Best Practices

### 1. Asynchronous programming

**All property getters and method callbacks must be asynchronous functions:**

```python
# Correct async properties
async def get_power(self):
    return self.power

# Correct asynchronous method
async def turn_on(self, params):
    self.power = True
    return {"status": "success"}

# Error: Synchronous function will throw exception
def get_power(self):  # TypeError!
    return self.power
```

### 2. Parameter processing

**Correct handling of required and optional parameters:**

```python
async def my_method(self, params):
# Process required parameters
    required_value = params["required_param"].get_value()
    
# Handle optional parameters
    optional_value = None
    if "optional_param" in params:
        optional_value = params["optional_param"].get_value()
    
# Parameter validation
    if not isinstance(required_value, str):
return {"status": "error", "message": "Wrong parameter type"}
    
    return {"status": "success", "result": required_value}
```

### 3. Error handling

**Implement proper error handling:**

```python
async def risky_operation(self, params):
    try:
# Perform operations that may fail
        result = await self.perform_operation()
        return {"status": "success", "result": result}
    except ValueError as e:
return {"status": "error", "message": f"Parameter error: {e}"}
    except Exception as e:
logger.error(f"Operation failed: {e}", exc_info=True)
return {"status": "error", "message": "Operation failed"}
```

### 4. Resource Management

**Properly manage device resources:**

```python
class MyDevice(Thing):
    def __init__(self):
super().__init__("MyDevice", "My device")
        self.resource = None
        self._lock = asyncio.Lock()
    
    async def acquire_resource(self, params):
        async with self._lock:
            if self.resource is None:
                self.resource = await self.create_resource()
            return {"status": "success"}
    
    async def cleanup(self):
"""Device cleaning method"""
        if self.resource:
            await self.resource.close()
            self.resource = None
```

### 5. Logging

**Use a unified logging system:**

```python
from src.utils.logging_config import get_logger

class MyDevice(Thing):
    def __init__(self):
super().__init__("MyDevice", "My device")
        self.logger = get_logger(self.__class__.__name__)
    
    async def my_method(self, params):
self.logger.info("Method was called")
        try:
            result = await self.perform_operation()
self.logger.info(f"Operation successful: {result}")
            return {"status": "success", "result": result}
        except Exception as e:
self.logger.error(f"Operation failed: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}
```

## Migration instructions

**Important note**: The project is migrating from IoT device mode to MCP (Model Context Protocol) tool mode:

1. **Countdown Timer**: Migrated to MCP tool to provide better AI integration
2. **Other devices**: May be migrated gradually depending on complexity
3. **New Feature**: It is recommended to consider using the MCP tool framework directly

The current IoT architecture is still stable and available, suitable for:

- Simple device control
- Learn and demonstrate
- Rapid prototyping

## Notes

1. **Asynchronous requirements**: All property getters and method callbacks must be asynchronous functions
2. **Parameter processing**: Method parameters are passed through Parameter objects, and you need to call `get_value()` to obtain the value.
3. **Error Handling**: Implement appropriate error handling and feedback mechanisms
4. **Resource Management**: Manage device resources correctly to avoid resource leakage
5. **Device Name**: Ensure that the device name is globally unique
6. **Return format**: The method return should contain the `status` and `message` fields

## Summarize

py-xiaozhi's IoT architecture provides a complete device abstraction and management framework, supporting asynchronous operations, type safety and state management. By following the best practices in this guide, you can quickly develop stable and reliable IoT devices. As projects migrate to the MCP tooling model, it is recommended that new features consider using the MCP tooling framework.
