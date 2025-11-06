#12306Railway Tools

The train ticket query tool is an MCP tool set based on the 12306 system, which provides functions such as train ticket query, station information query, and transfer plan query. The tool provides two layers of interfaces: **Smart Tools** (user-friendly natural language interface) and **Atomic Tools** (technical development interface).

## Smart tools (recommended)

Smart tools can understand natural language input and automatically handle complex query logic, making them the preferred method for daily use.

### Common usage scenarios

**Smart train ticket inquiry:**
- "Check tomorrow's train tickets from Beijing to Shanghai"
- "I want to see the high-speed train from Guangzhou to Shenzhen the day after tomorrow."
- "Help me check the tickets from Hangzhou to Nanjing this Saturday"
- "Query the train from Beijing South to Tianjin on January 15, 2025"
- "What are the high-speed trains departing from Shanghai in the morning?"

**Smart Station Query:**
- "What train stations are there in Beijing?"
- "Which is the main train station in Shanghai?"
- "Query the station code of Beijing South Railway Station"
- "Detailed information of Hongqiao Station"

**Intelligent transfer query:**
- "What should I do if there is no direct train from Beijing to Guangzhou?"
- "Check the transfer plan from Harbin to Kunming"
- "I need to transfer in Zhengzhou, help me check the ticket"

**Smart travel suggestions:**
- "What's the best way to get from Beijing to Shanghai"
- "Recommend to me a travel plan from Guangzhou to Shenzhen"
- "I want the fastest way to go to Hangzhou"
- "Recommended affordable train tickets"

### Usage tips

1. **Use common city names**: such as "Beijing", "Shanghai", "Guangzhou", etc., the system will automatically match major stations
2. **Provide specific dates**: Support relative times such as "tomorrow", "the day after tomorrow", "this Saturday", etc.
3. **Specified car model preference**: You can indicate your preference for high-speed rail, high-speed train or ordinary train
4. **Consider travel time**: You can specify the departure time period, such as "morning", "afternoon", etc.
5. **Express preferences**: You can explain preferences such as "fastest", "cheapest", "comfortable", etc.

The AI ​​assistant will automatically call intelligent tools based on your needs to provide you with accurate ticket information and travel suggestions.

## Detailed introduction of smart tools

### 1. smart_ticket_query - Smart train ticket query
Automatically process natural language train ticket queries, supporting relative dates, car model preferences, time period filtering, etc.

**Features:**
- Automatically convert city name to station code
- Support relative dates (tomorrow, the day after tomorrow, this Saturday, etc.)
- Intelligent recognition of car model preferences (high-speed rail, high-speed train, direct train, etc.)
- Filter by time period (morning, afternoon, evening)
- Formatted output for easy reading

**Usage example:**
- "Check tomorrow's train tickets from Beijing to Shanghai"
- "I want to see the high-speed train from Guangzhou to Shenzhen the day after tomorrow."
- "What trains depart to Nanjing in the morning?"

### 2. smart_transfer_query - Smart transfer query
When there is no direct train, the optimal transfer plan is automatically found and detailed transfer information is provided.

**Features:**
- Automatically calculate the optimal transfer route
- Display transfer waiting time
- Support designated transit cities
-Analyze same-station transfers and cross-station transfers
- Provide complete itinerary information

**Usage example:**
- "What should I do if there is no direct train from Beijing to Guangzhou?"
- "Check the transfer plan from Harbin to Kunming"
- "I need to transfer in Zhengzhou, help me check the ticket"

### 3. smart_station_query - smart station query
Handle various station-related queries, automatically identify query intentions and provide corresponding information.

**Features:**
- Automatically identify query types (station list, main stations, coding, etc.)
-Support city station query
- Provide station details
- Intelligent analysis of query intent

**Usage example:**
- "What train stations are there in Beijing?"
- "Which is the main train station in Shanghai?"
- "Query the station code of Beijing South Railway Station"

### 4. smart_travel_suggestion - Smart travel suggestions
Comprehensive analysis of direct and transfer options, and personalized travel suggestions based on user preferences.

**Features:**
- Comprehensive analysis of various travel options
- Recommend the best solution based on preferences
- Provide detailed pros and cons analysis
- Support time and price optimization
- Reasons for personalized recommendations

**Usage example:**
- "What's the best way to get from Beijing to Shanghai"
- "Recommend to me a travel plan from Guangzhou to Shenzhen"
- "I want the fastest way to go to Hangzhou"

## Function overview

### Station information query
- **City Station Query**: Query all train stations in the specified city
- **Station code query**: Get the 12306 code of the station
- **Station Name Query**: Get detailed information based on the station name
- **Main Station Identification**: Automatically identify the main stations of the city

### Train ticket inquiry
- **Direct ticket inquiry**: Inquiry for direct trains between two places
- **Fare Information**: Displays prices and remaining tickets for various seat types
- **Train number filtering**: Supports filtering by car type, time and other conditions
- **Sort function**: Supports sorting by departure time, price, etc.

### Transfer plan query
- **Smart Transfer**: Automatically calculate the optimal transfer plan
- **Transfer Time**: Displays transfer waiting time
- **Transfer Station**: Supports designated transfer stations
- **Total Duration**: Calculate the total travel time including transfers

### Practical functions
- **Date Management**: Get the current date and support relative time query
- **Vote Quantity Status**: Real-time display of remaining votes
- **Special Mark**: Show train characteristics (such as sleeper, dining car, etc.)

## Atomic Tools (Developer Interface)

Atomic tools provide underlying technical interfaces and are suitable for system integration and secondary development. Each atomic tool implements a single function and requires precise parameter input.

### Basic information tools

#### get_current_date - Get the current date
Get the current date (Shanghai time zone).

**parameter:**
none

**Usage scenario:**
- Confirm current date
- Relative time calculation
- Date verification

#### get_stations_in_city - Get city stations
Get all train station information in a specified city.

**parameter:**
- `city` (required): city name

**Usage scenario:**
- View all stations in the city
- Select a specific station
- Understand the distribution of stations

#### get_city_station_code - Get the main station code of the city
Get coding information for the city's major stations.

**parameter:**
- `cities` (required): city name, multiple cities separated by "|"

**Usage scenario:**
- Quickly access major stations
- Query city stations in batches
- System integration

#### get_station_by_name - query based on station name
Get detailed information based on station name.

**parameter:**
- `station_names` (required): Station names, multiple stations separated by "|"

**Usage scenario:**
- Verify station name
- Get station details
-Confirmation of station information

#### get_station_by_code - query based on station code
Get station information based on station code.

**parameter:**
- `station_code` (required): station code

**Usage scenario:**
- Coding anti-checking station
- System data verification
- Technology integration

### 2. Train ticket query tool

#### query_train_tickets - Query train tickets
Query train ticket information for a specified date and section.

**parameter:**
- `date` (required): departure date, format "YYYY-MM-DD"
- `from_station` (required): departure station
- `to_station` (required): Arrival station
- `train_filters` (optional): train filter conditions
- `sort_by` (optional): sorting method
- `reverse` (optional): whether to reverse order
- `limit` (optional): limit on the number of results

**Usage scenario:**
- Daily travel ticket checking
- Fare comparison
- Travel planning

#### query_transfer_tickets - Query transfer tickets
Inquire about train ticket options that require transfers.

**parameter:**
- `date` (required): departure date
- `from_station` (required): departure station
- `to_station` (required): Arrival station
- `middle_station` (optional): Specify the transfer station
- `show_wz` (optional): whether to display no seats
- `train_filters` (optional): train filter conditions
- `sort_by` (optional): sorting method
- `reverse` (optional): whether to reverse order
- `limit` (optional): limit on the number of results, default 10

**Usage scenario:**
- Check transfers when there is no direct train
- Compare transfer options
- Complex travel planning

#### query_train_route - Query train stops
Query the stop information of the specified train.

**parameter:**
- `train_code` (required): train number

**Usage scenario:**
- Know the bus route
- Choose an intermediate site
- Travel route planning

Note: This feature is under development

## Usage example

### Basic information query example

```python
# Get the current date
result = await mcp_server.call_tool("get_current_date", {})

# Query all stations in Beijing
result = await mcp_server.call_tool("get_stations_in_city", {
"city": "Beijing"
})

# Get major stations in multiple cities
result = await mcp_server.call_tool("get_city_station_code", {
"cities": "Beijing|Shanghai|Guangzhou"
})

# Query based on station name
result = await mcp_server.call_tool("get_station_by_name", {
"station_names": "Beijing South|Shanghai Hongqiao"
})

# Query based on station code
result = await mcp_server.call_tool("get_station_by_code", {
    "station_code": "VNP"
})
```

### Train ticket query example

```python
#Basic train ticket query
result = await mcp_server.call_tool("query_train_tickets", {
    "date": "2025-07-15",
"from_station": "Beijing",
"to_station": "Shanghai"
})

#Query with filter conditions
result = await mcp_server.call_tool("query_train_tickets", {
    "date": "2025-07-15",
"from_station": "Beijing",
"to_station": "Shanghai",
"train_filters": "G,D", # Only search high-speed trains and high-speed trains
    "sort_by": "departure_time",
    "limit": 10
})

# Transfer ticket inquiry
result = await mcp_server.call_tool("query_transfer_tickets", {
    "date": "2025-07-15",
"from_station": "Beijing",
"to_station": "Guangzhou",
    "limit": 5
})

#Specify transfer station query
result = await mcp_server.call_tool("query_transfer_tickets", {
    "date": "2025-07-15",
"from_station": "Beijing",
"to_station": "Guangzhou",
"middle_station": "Zhengzhou",
    "limit": 5
})
```

## Data structure

### Station information (Station)
```python
{
    "station_code": "VNP",
"station_name": "Beijing South",
    "station_pinyin": "beijingnan",
"city": "Beijing",
    "code": "VNP"
}
```

### Train ticket information (Ticket)
```python
{
    "start_train_code": "G1",
"from_station": "Beijing South",
"to_station": "Shanghai Hongqiao",
    "start_time": "09:00",
    "arrive_time": "14:28",
    "duration": "5:28",
    "prices": [
        {
"seat_name": "Business Seat",
            "price": "1748",
            "num": "3"
        },
        {
"seat_name": "First class seat",
            "price": "933",
"num": "yes"
        }
    ],
"features": ["WiFi", "Charging socket"]
}
```

### Transfer plan (Transfer)
```python
{
    "start_date": "2025-07-15",
    "start_time": "08:00",
    "arrive_date": "2025-07-15",
    "arrive_time": "20:30",
"from_station_name": "Beijing South",
"middle_station_name": "Zhengzhou East",
"end_station_name": "Guangzhou South",
    "same_train": false,
    "same_station": true,
"wait_time": "2 hours and 15 minutes",
"duration": "12 hours and 30 minutes",
    "ticket_list": [
        {
            "start_train_code": "G79",
"from_station": "Beijing South",
"to_station": "Zhengzhou East",
            "start_time": "08:00",
            "arrive_time": "11:15",
            "duration": "3:15",
            "prices": [...]
        }
    ]
}
```

## Ticket volume status description

### Remaining votes display
- **Specific numbers**: For example, "5" means there are 5 tickets left
- **"有"**: There are tickets, but the specific number is unknown
- **"Sufficient"**: Sufficient tickets
- **"None"**: No ticket
- **"--"**: This seat type is not available for sale
- **"Waiting"**: No tickets, waiting available

### Seat type
- **Business Class**: The highest class seat
- **First Class**: High class seats
- **Second Class**: Standard seat
- **No seats**: Standing ticket
- **Hard Sleeper**: Hard Sleeper
- **Soft sleeper**: Soft sleeper
- **Superior Soft Sleeper**: Deluxe Sleeper

## Query skills

### 1. Station name
- Use official station names, such as "Beijing South" instead of "Beijing South Railway Station"
- Support city names, the system will automatically match major stations
- There may be multiple candidates for major stations. It is recommended to specify the station name.

### 2. Time format
- Date format: YYYY-MM-DD, such as "2025-07-15"
- Support relative time, such as "tomorrow", "the day after tomorrow"
- Pay attention to holidays and holiday arrangements

### 3. Filter conditions
- Train selection: G (high-speed rail), D (motor train), C (intercity), Z (direct), T (express), K (express)
- Time filter: sort by departure time or arrival time
- Price filter: sort by ticket price

### 4. Transit query
- Priority transfer at major hubs
- Pay attention to the transfer time and it is recommended to reserve sufficient transfer time
- Consider luggage and travel convenience

## Notes

1. **Real-time data**: Ticketing information is updated in real time, and the query results are for reference only.
2. **Ticket Purchase Channel**: The tool only provides query function, and tickets must be purchased through official channels.
3. **Network dependency**: The query requires a network connection to the 12306 system
4. **Query Limitations**: Avoid frequent queries and comply with 12306 usage specifications

## troubleshooting

### FAQ
1. **Incorrect station name**: Check whether the station name is correct
2. **No results found**: Confirm date and station information
3. **Network Timeout**: Check network connection status
4. **Data format error**: Verify input parameter format

### Debugging method
1. First check the station information to confirm the station name
2. Use get_current_date to confirm the date format
3. Check network connections and firewall settings
4. View the returned error message

## Secondary Development Guide

### MCP Tool Integration

Railway tools are based on the MCP (Model Context Protocol) architecture and support flexible tool integration and expansion.

#### Tool Manager
```python
from src.mcp.tools.railway import get_railway_tools_manager

# Get tool manager instance
manager = get_railway_tools_manager()

# Initialization tool (called in MCP server)
manager.init_tools(add_tool, PropertyList, Property, PropertyType)
```

#### Custom smart tools
Developers can create new smart tools based on existing atomic tools:

```python
async def custom_smart_query(self, args: Dict[str, Any]) -> str:
"""Customized intelligent query tool"""
# Parse user input
    query = args.get("query", "")
    
# Call atomic tools
    client = await get_railway_client()
    result = await client.query_tickets(...)
    
# Format output
    return self._format_custom_result(result)
```

### Architecture description

Railway tools adopt a layered architecture:
- **Intelligent Tool Layer**: Processes natural language input, user-friendly
- **Atomic Tool Layer**: Provides basic functions and technical accuracy
- **Client Layer**: Interacting with 12306 API
- **Data Model Layer**: Define data structure

### Extension suggestions

1. **Add new smart tools**: combine new functions based on existing atomic tools
2. **Optimize query logic**: Improve the processing algorithm of intelligent tools
3. **Enhanced Data Format**: Add more output format options
4. **Integrate other services**: Combine with other transportation information

Through the train ticket query tool, you can easily obtain train ticket information and plan travel routes. It is an essential and practical tool for travel. Smart tools make daily use more convenient, and atomic tools provide developers with powerful integration capabilities.