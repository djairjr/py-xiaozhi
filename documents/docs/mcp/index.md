# MCP Development Guide

MCP (Model Context Protocol) is an open standard protocol for AI tool extension. This project implements a powerful tool system based on MCP, supporting the seamless integration of multiple functional modules.

## 📖 Document Navigation

- **[🔧Built-in MCP Development Guide](#SystemArchitecture)** - This document: Develop and use built-in MCP tools
- **[🔌 External MCP Access Guide](xiaozhi-mcp.md)** - External MCP service access and community project integration

> 💡 **Selection Guide**: If you want to develop new built-in tools, please refer to this document; if you want to access external MCP services or learn about community projects, please view the [Plug-in Access Guide] (xiaozhi-mcp.md).

## System architecture

### Core components

#### 1. MCP server (`src/mcp/mcp_server.py`)
- **Based on JSON-RPC 2.0 protocol**: Comply with MCP standard specification
- **Single case mode**: Global unified server instance management
- **Tool Registration System**: Supports dynamic addition and management of tools
- **Parameter Validation**: Complete type checking and parameter validation mechanism
- **Error Handling**: Standardized error response and exception handling

#### 2. Tool attribute system
```python
#Attribute type definition
class PropertyType(Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    STRING = "string"

#Property definition
@dataclass
class Property:
    name: str
    type: PropertyType
    default_value: Optional[Any] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
```

#### 3. Tool definition structure
```python
@dataclass
class McpTool:
name: str # Tool name
description: str # tool description
properties: PropertyList # Parameter list
callback: Callable # callback function
```

### Tool Manager Architecture

Each functional module has a corresponding manager class, which is responsible for:
- Initialization and registration of tools
- Encapsulation of business logic
- Interaction with underlying services

#### Existing tool modules

1. **System tools (`src/mcp/tools/system/`)**
- Equipment status monitoring
- Application management (start, terminate, scan)
- System information query

2. **Schedule Management (`src/mcp/tools/calendar/`)**
- Add, delete, modify and check the schedule
- Intelligent time analysis
- Clash detection
- Reminder service

3. **Timer (`src/mcp/tools/timer/`)**
- Countdown timer management
- Task scheduling
- Time reminder

4. **Music player (`src/mcp/tools/music/`)**
- Music playback control
- Playlist management
- Volume control

5. **Railway query (`src/mcp/tools/railway/`)**
- 12306 train number query
- Station information query
- Fare inquiry

6. **Search tool (`src/mcp/tools/search/`)**
- Web search
- Information retrieval
- Filter results

7. **Recipe Tool (`src/mcp/tools/recipe/`)**
- Recipe query
- Recipe recommendations
- Nutritional information

8. **Camera Tools (`src/mcp/tools/camera/`)**
- Photo function
- Visual Q&A
- Image analysis

9. **Map Tools (`src/mcp/tools/amap/`)**
- Geocoding/reverse geocoding
- Path planning
- Weather query
- POI search

10. **Bazi numerology (`src/mcp/tools/bazi/`)**
- Bazi calculation
- Numerology analysis
- Intermarriage analysis
- Almanac query

## Tool Development Guide

### 1. Create a new tool module

Creating a new tool module requires the following steps:

#### Step 1: Create module directory
```bash
mkdir src/mcp/tools/your_tool_name
cd src/mcp/tools/your_tool_name
```

#### Step 2: Create necessary files
```bash
touch __init__.py
touch manager.py # Manager class
touch tools.py # Tool function implementation
touch models.py #Data model (optional)
touch client.py # Client class (optional)
```

#### Step 3: Implement the manager class
```python
# manager.py
class YourToolManager:
    def __init__(self):
#Initialization code
        pass
    
    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
Initialize and register tools
        """
# Define tool properties
        tool_props = PropertyList([
            Property("param1", PropertyType.STRING),
            Property("param2", PropertyType.INTEGER, default_value=0)
        ])
        
#Registration tool
        add_tool((
            "tool_name",
"Tool Description",
            tool_props,
            your_tool_function
        ))

# Global manager instance
_manager = None

def get_your_tool_manager():
    global _manager
    if _manager is None:
        _manager = YourToolManager()
    return _manager
```

#### Step 4: Implement tool functions
```python
# tools.py
async def your_tool_function(args: dict) -> str:
    """
Tool function implementation
    """
    param1 = args.get("param1")
    param2 = args.get("param2", 0)
    
#Business logic
    result = perform_operation(param1, param2)
    
return f"Operation result: {result}"
```

#### Step 5: Register to the main server
Add in the `add_common_tools` method of `src/mcp/mcp_server.py`:
```python
# Add your tools
from src.mcp.tools.your_tool_name import get_your_tool_manager

your_tool_manager = get_your_tool_manager()
your_tool_manager.init_tools(self.add_tool, PropertyList, Property, PropertyType)
```

### 2. Best Practices

#### Tool naming convention
- Use `self.module.action` format
- For example: `self.calendar.create_event`, `self.music.play`

#### Parameter design
- Required parameters do not have default values
- Optional parameters set to sensible default values
- Use appropriate parameter types (STRING, INTEGER, BOOLEAN)

#### Error handling
```python
async def your_tool_function(args: dict) -> str:
    try:
#Business logic
        result = await perform_operation(args)
return f"Success: {result}"
    except Exception as e:
logger.error(f"Tool execution failed: {e}")
return f"Error: {str(e)}"
```

#### Asynchronous support
- Prefer async/await
- Support automatic packaging of synchronized functions
- Proper use of asyncio tools

### 3. Writing tool description

Tool description should contain:
- Function introduction
- Usage scenarios
- Parameter description
- return format
- Precautions

Example:
```python
description = """
Create new schedule events with support for intelligent time setting and conflict detection.
Usage scenarios:
1. Schedule a meeting or appointment
2. Set reminders
3. Time management planning

parameter:
title: event title (required)
start_time: start time, ISO format (required)
end_time: end time, can be automatically calculated
description: event description
category: event classification
reminder_minutes: reminder time (minutes)

Return: creation success or failure message
"""
```

## Usage example

### Schedule Management
```python
#Create schedule
await mcp_server.call_tool("self.calendar.create_event", {
"title": "Team Meeting",
    "start_time": "2024-01-01T10:00:00",
"category": "Conference",
    "reminder_minutes": 15
})

# Check today’s schedule
await mcp_server.call_tool("self.calendar.get_events", {
    "date_type": "today"
})
```

### Map function
```python
#Convert address to latitude and longitude
await mcp_server.call_tool("self.amap.geocode", {
"address": "Tiananmen Square, Beijing"
})

# Path planning
await mcp_server.call_tool("self.amap.direction_walking", {
    "origin": "116.397428,39.90923",
    "destination": "116.390813,39.904368"
})
```

### Eight-character numerology
```python
# Get horoscope analysis
await mcp_server.call_tool("self.bazi.get_bazi_detail", {
    "solar_datetime": "2008-03-01T13:00:00+08:00",
    "gender": 1
})

# marriage analysis
await mcp_server.call_tool("self.bazi.analyze_marriage_compatibility", {
    "male_solar_datetime": "1990-01-01T10:00:00+08:00",
    "female_solar_datetime": "1992-05-15T14:30:00+08:00"
})
```

## Advanced features

### 1. Parameter verification
The system provides a complete parameter verification mechanism:
- type checking
- Range validation
- Required parameter check
- Default value handling

### 2. Tool discovery
Support dynamic tool discovery and list acquisition:
- Pagination support
- size limit
- Cursor traversal

### 3. Visual ability
Support visual related functions:
- Image analysis
- Visual Q&A
- Configure external vision services

### 4. Concurrent processing
- Asynchronous tool execution
- Task scheduling
- Resource management

## Debugging and testing

### Log system
```python
from src.utils.logging_config import get_logger
logger = get_logger(__name__)

logger.info("Tool execution starts")
logger.error("Execution failed", exc_info=True)
```

### Test Tools
```python
# Test tool registration
server = McpServer.get_instance()
server.add_common_tools()

# Test tool call
result = await server.parse_message({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "your_tool_name",
        "arguments": {"param1": "value1"}
    },
    "id": 1
})
```

## Deployment and configuration

### Environmental requirements
- Python 3.8+
- Asynchronous support
- Relevant dependent libraries

### Configuration file
Tool configuration is managed through `config/config.json` and supports:
- API key configuration
- Service endpoint settings
- Function switch control

### Performance optimization
- Connection pool management
- Caching strategy
- Concurrency control
- Resource recovery

## troubleshooting

### FAQ
1. **Tool registration failed**: Check manager singleton and import path
2. **Parameter validation error**: Confirm parameter type and necessity
3. **Asynchronous call issue**: Make sure to use async/await correctly
4. **Missing dependency**: Check module import and dependency installation

### Debugging Tips
- Enable verbose logging
- Use debugging tools
- Unit test verification
- Performance analysis tools
