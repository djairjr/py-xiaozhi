# Amap Tools

The Amap Map Tool is an MCP tool set based on the Amap Web API, which provides a wealth of geographical location service functions.

## How to use natural language

### Route planning
- "How to get from Yunsheng Science Park to Science City Metro Station"
- "Route to Tianhe City"
- "How long does it take to drive from A to B"

### Recent location query
- "How to get to the nearest milk tea shop"
- "Where is the nearest restaurant?"
- "Nearest metro station"
- "Nearest bank"

### Search nearby places
- "What milk tea shops are nearby?"
- "Nearby restaurants"
- "Supermarkets nearby"
- "Nearby banks within 2 kilometers"

### Intelligent Navigation
- "Go to Tianhe City"
- "Navigate to Canton Tower"
- "How to get to Baiyun Airport"

### Comparison of travel modes
- "Which is faster from A to B, driving or taking the subway?"
- "Compare the various ways to get to the airport"
- "Which way is fastest"

## MCP tool introduction

### Smart tools (recommended)

#### 1. route_planning - Intelligent route planning
Support route planning for natural language address input and automatically handle address conversion and coordinate parsing.

**parameter:**
- `origin` (required): origin address name
- `destination` (required): destination address name
- `city` (optional): the city where you are located, the default is Guangzhou
- `travel_mode` (optional): travel mode, walking (walking), driving (driving), bicycling (cycling), transit (bus), the default is walking

#### 2. find_nearest - nearest location search
Finds the nearest location of a certain type and provides detailed walking directions.

**parameter:**
- `keywords` (required): search keywords, such as "milk tea shop", "restaurant", "subway station", "bank"
- `radius` (optional): search radius (meters), default 5000 meters
- `user_location` (optional): user location, if not provided, it will be automatically located

#### 3. find_nearby - Search for nearby places
Search multiple nearby places and display them sorted by distance.

**parameter:**
- `keywords` (required): search keywords, such as "milk tea shop", "restaurant", "supermarket"
- `radius` (optional): search radius (meters), default 2000 meters
- `user_location` (optional): user location, if not provided, it will be automatically located

#### 4. navigation - intelligent navigation
Provides comparison and recommendations of various travel modes to your destination.

**parameter:**
- `destination` (required): destination name
- `city` (optional): the city where you are located, the default is Guangzhou
- `user_location` (optional): user location, if not provided, it will be automatically located

#### 5. get_location - Get the current location
Intelligent positioning service based on IP address.

**parameter:**
- `user_ip` (optional): User IP address, automatically obtained if not provided

#### 6. compare_routes - Route comparison
Compare the time, distance and suitability of different travel modes.

**parameter:**
- `origin` (required): origin address name
- `destination` (required): destination address name
- `city` (optional): the city where you are located, the default is Guangzhou

### Basic tools (for secondary development)

#### Geocoding Tools
- `maps_geo` - Convert address to coordinates
- `maps_regeocode` - coordinates to address
- `maps_ip_location` - IP location

#### Path planning tool
- `maps_direction_walking` - walking path planning
- `maps_direction_driving` - Driving route planning
- `maps_bicycling` - Cycling route planning
- `maps_direction_transit_integrated` - bus route planning

#### Search Tools
- `maps_text_search` - keyword search
- `maps_around_search` - surrounding search
- `maps_search_detail` - POI details query

#### Other tools
- `maps_weather` - weather query
- `maps_distance` - distance measurement

## Usage example

### Smart Tool Example

```python
# Intelligent route planning
result = await mcp_server.call_tool("route_planning", {
"origin": "Yunsheng Science Park",
"destination": "Science City Metro Station",
    "travel_mode": "walking"
})

# Find recent locations
result = await mcp_server.call_tool("find_nearest", {
"keywords": "milk tea shop",
    "radius": "5000"
})

# Search nearby places
result = await mcp_server.call_tool("find_nearby", {
"keywords": "restaurant",
    "radius": "2000"
})
```

### Basic tool example

```python
# Convert address to coordinates
result = await mcp_server.call_tool("maps_geo", {
"address": "Beijing Tiananmen Square",
"city": "Beijing"
})

# Walking path planning
result = await mcp_server.call_tool("maps_direction_walking", {
    "origin": "116.397428,39.90923",
    "destination": "116.390813,39.904368"
})
```

## Secondary development instructions

### Tool architecture

Amap’s map tool adopts a layered architecture design:

#### 1. Intelligent tool layer (MCP adaptation)
- **AmapToolsManager**: Manager for adapting MCP servers
- **Smart Tool Registration**: Automatically register user-friendly smart tools
- **Parameter Validation**: Complete parameter type and format validation
- **Result Formatting**: User-friendly result display

#### 2. Business logic layer (AmapManager)
- **Intelligent route planning**: Supports natural language address input
- **Automatic Positioning**: Multi-strategy IP positioning and city identification
- **Combined Functions**: Combine multiple API calls into advanced functions
- **Error Handling**: Complete exception handling and fault tolerance mechanism

#### 3. API client layer (AmapClient)
- **HTTP Client**: Asynchronous HTTP client based on aiohttp
- **API Encapsulation**: A complete encapsulation of all Amap APIs
- **Response Parsing**: Automatically parse API responses and convert them into data models
- **Error Handling**: API level error handling and retries

#### 4. Data model layer (Models)
- **Structured data**: Data structure defined using dataclass
- **Type Safety**: Complete type annotations and validation
- **Format Conversion**: Automatic conversion of coordinates, addresses and other formats
- **Data consistency**: unified data format and naming convention

### Intelligent features

#### Automatic positioning strategy
1. Prioritize the use of AutoNavi API automatic IP identification
2. If that fails, try a third-party IP service
3. Verify the validity of positioning results
4. Return to city center coordinates

#### Intelligent address resolution
- Support natural language address input: "Tiananmen Square"
- Supported coordinate format: "116.397428,39.90923"
- Support composite address: "No. 1 Tiananmen Square, Dongcheng District, Beijing"

#### Intelligent formatting of results
- User friendly output format
- Comparative display of multiple travel modes
- Detailed walking route guidance

### Configuration instructions

#### API key configuration
The Amap map tool requires an API key to be configured for normal use.

**Get API key:**
1. Visit [Amap Open Platform](https://lbs.amap.com/)
2. Register a developer account
3. Create an application and obtain the API Key

**Configuration method:**
Currently the API key is hardcoded in `src/mcp/tools/amap/__init__.py`:

```python
AMAP_API_KEY = "your_api_key_here"
```

**Recommended configuration method:**
Configure the API key into `config/config.json`:

```json
{
  "amap": {
    "api_key": "your_api_key_here"
  }
}
```

### Extension development

#### Add new smart tools
1. Implement business logic in `AmapManager`
2. Register new tools in `AmapToolsManager`
3. Add tool definition in `AmapTools`
4. Update test cases

#### Add new basic tools
1. Encapsulate API calls in `AmapClient`
2. Implement business logic in `AmapManager`
3. Add tool definition in `AmapTools`
4. Update the data model (if necessary)

### Data structure

```python
@dataclass
class Location:
longitude: float # longitude
latitude: float # Latitude

@dataclass
class POI:
    id: str              # POI ID
name: str # name
address: str # address
location: Location # coordinates
type_code: str # Type code
```

### Best Practices

1. **Prioritize the use of smart tools**: automatically handle complex logic, user-friendly
2. **Set parameters reasonably**: Specify city, radius and other parameters to improve accuracy
3. **Error handling**: Handle network exceptions and API errors
4. **Caching Strategy**: Cache the results of frequent queries
5. **Asynchronous call**: Use asynchronous methods to improve performance

Through the AMAP map tool, you can easily add powerful geolocation service functions to your application to provide a better user experience.