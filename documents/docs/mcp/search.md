#Search Tools

The search tool is an intelligent network search MCP tool set that provides network search, content acquisition, result caching and other functions to help users quickly obtain Internet information.

### Common usage scenarios

**Daily information search:**
- "Search for today's weather"
- "Check the distance between Beijing and Shanghai"
- "Find the latest news"
- "Search for the latest developments in artificial intelligence"

**Learning and Research:**
- "Search for information about quantum computing"
- "Check the basic concepts of machine learning"
- "Find some Python programming tutorials"
- "Search for what happened today in history"

**Shopping price comparison:**
- "Search iPhone 15 price"
- "Check laptop recommendations"
- "Find some cost-effective mobile phones"
- "Search for the latest promotions"

**Life Services:**
- "Search for nearby restaurants"
- "Check train ticket booking information"
- "Find a decoration company"
- "Search for weekend activity recommendations"

**Technical Issues:**
- "Search for Python error solutions"
- "Query API interface documentation"
- "Look for software installation tutorials"
- "Search code examples"

### Usage tips

1. **Clear search intent**: Clearly describe what you are searching for
2. **Use Keywords**: Providing accurate keywords helps to get better results
3. **Specified quantity**: You can request that a specific number of search results be returned
4. **Deep Understanding**: You can request detailed content of a specific web page
5. **Multiple searches**: Further searches can be performed based on the search results.

The AI ​​assistant will automatically call the search tool based on your needs to provide you with accurate network information.

## Function overview

### Network search function
- **Bing Search**: Intelligent search based on Bing search engine
- **Multi-language support**: Supports search in multiple languages ​​such as Chinese and English
- **Regional Settings**: Support search results in different regions
- **Result Quantity Control**: You can set the number of returned results

### Content acquisition function
- **Web content crawl**: Get the detailed content of the search results page
- **Content length control**: You can limit the length of the obtained content
- **Smart Extraction**: Automatically extract the main content of the web page
- **Formatted Output**: Return content in a human-readable format

### Cache management function
- **Search results cache**: Automatically cache search results
- **Session Management**: Supports multiple search sessions
- **Cached query**: You can view historical search results
- **Cache Cleaning**: Support clearing search cache

### Session management function
- **Session Tracking**: Track search session status
- **Session Information**: Provides session details
- **Session Switching**: Supports switching of multiple search sessions
- **Session Persistence**: Save search session data

## Tool list

### 1. Search tool

#### search_bing - Bing search
Perform a Bing search to get information about the web.

**parameter:**
- `query` (required): search keyword
- `num_results` (optional): Number of results returned, default 5, maximum 10
- `language` (optional): search language, default "zh-cn"
- `region` (optional): search region, default "CN"

**Usage scenario:**
- Daily information search
- Study and research
- News inquiry
- Technical problem solving

### 2. Content acquisition tool

#### fetch_webpage_content - Get web page content
Get the web page details of the specified search results.

**parameter:**
- `result_id` (required): search result ID
- `max_length` (optional): Maximum content length, default 8000, maximum 20000

**Usage scenario:**
- Read in-depth web content
- Get article details
- Analyze web page information
- Content research

### 3. Cache management tool

#### get_search_results - Get search results cache
Get cached search results.

**parameter:**
- `session_id` (optional): session ID

**Usage scenario:**
- View historical search results
- Review search history
- Session management
- Compare results

#### clear_search_cache - clear search cache
Clear all search cache data.

**parameter:**
none

**Usage scenario:**
- Clear search history
- Reset search status
- Free up memory space
- Privacy protection

### 4. Session management tool

#### get_session_info - Get session information
Get details of the current search session.

**parameter:**
none

**Usage scenario:**
- View session status
- Session statistics
- System monitoring
- debugging information

## Usage example

### Basic search example

```python
#Basic search
result = await mcp_server.call_tool("search_bing", {
"query": "Latest developments in artificial intelligence",
    "num_results": 5
})

#Search for specified language and region
result = await mcp_server.call_tool("search_bing", {
    "query": "artificial intelligence",
    "num_results": 10,
    "language": "en-us",
    "region": "US"
})

# Get web content
result = await mcp_server.call_tool("fetch_webpage_content", {
    "result_id": "search_result_123",
    "max_length": 10000
})
```

### Cache management example

```python
# Get the search result cache
result = await mcp_server.call_tool("get_search_results", {})

# Get search results for a specific session
result = await mcp_server.call_tool("get_search_results", {
    "session_id": "session_123"
})

# Clear search cache
result = await mcp_server.call_tool("clear_search_cache", {})
```

### Session management example

```python
# Get session information
result = await mcp_server.call_tool("get_session_info", {})
```

## Data structure

### Search Results (SearchResult)
```python
{
    "id": "search_result_123",
"title": "The latest development trends of artificial intelligence",
    "url": "https://example.com/ai-trends",
"snippet": "Artificial intelligence technology has achieved major breakthroughs in 2025...",
    "source": "example.com",
    "has_content": true,
    "created_at": "2025-01-15T10:30:00Z"
}
```

### Search Response (SearchResponse)
```python
{
    "success": true,
"query": "Latest developments in artificial intelligence",
    "num_results": 5,
    "results": [
        {
            "id": "search_result_123",
"title": "The latest development trends of artificial intelligence",
            "url": "https://example.com/ai-trends",
"snippet": "Artificial intelligence technology has achieved major breakthroughs in 2025...",
            "source": "example.com"
        }
    ],
    "session_info": {
        "session_id": "session_123",
        "created_at": "2025-01-15T10:25:00Z",
        "total_searches": 1,
        "total_results": 5
    }
}
```

### Webpage Content (WebpageContent)
```python
{
    "success": true,
    "result_id": "search_result_123",
    "result_info": {
        "id": "search_result_123",
"title": "The latest development trends of artificial intelligence",
        "url": "https://example.com/ai-trends",
"snippet": "Artificial intelligence technology has achieved major breakthroughs in 2025...",
        "source": "example.com"
    },
"content": "Artificial intelligence technology has made major breakthroughs in 2025, including large language models, computer vision, natural language processing and other fields...",
    "content_length": 5420
}
```

### Session Information (SessionInfo)
```python
{
    "session_id": "session_123",
    "created_at": "2025-01-15T10:25:00Z",
    "last_search_at": "2025-01-15T10:30:00Z",
    "total_searches": 3,
    "total_results": 15,
    "cached_results": 12,
    "status": "active"
}
```

##Search Tips

### 1. Keyword selection
- Use specific, accurate keywords
- Avoid search terms that are too broad
- Multiple keyword combinations can be used
- Try different expressions

### 2. Language and regional settings
- Chinese search: language="zh-cn", region="CN"
- English search: language="en-us", region="US"
- Choose the appropriate language based on the content source
- Locale affects the relevance of search results

### 3. Result quantity control
- General search: 5-10 results
- Dive deeper: 10 results
- Quick Browse: 3-5 results
- Avoid getting too many results at once

### 4. Content Acquisition Strategy
- Search first to get a list of results
- Select highly relevant results to obtain content
- Adjust content length as needed
- You can obtain the contents of multiple results for comparison

## Best Practices

### 1. Search strategy
- Gradually refine your search from broad to specific
- Use multiple keyword combinations
- Try different search angles
- Pay attention to the timeliness of search results

### 2. Content processing
- Obtain web page details as needed
- Set reasonable content length limits
- Pay attention to the source and reliability of the content
- Can obtain content from multiple sources for comparison

### 3. Cache utilization
- Take advantage of search result caching
- Clean unnecessary cache regularly
- Use session management features
- Pay attention to cache effectiveness

### 4. Privacy protection
- Clear cache promptly after sensitive searches
- Pay attention to the privacy of search content
- Proper use of session management functions
- Avoid searching for sensitive information

## Supported search types

### Information search
- News and information
- Academic information
- Encyclopedia knowledge
- Technical documentation

### Business Search
- Product information
- price comparison
- Business information
- Market analysis

### Life services
- local services
- Catering and entertainment
- Transportation
- Life guide

### Technical Support
- Programming questions
- Software usage
- Bug fixes
- Technical tutorials

## Notes

1. **Network dependency**: The search function requires a stable network connection
2. **Search Restrictions**: Comply with the usage specifications of search engines
3. **Content Accuracy**: The accuracy of search results relies on the original source
4. **Copyright Issues**: Pay attention to the copyright and usage restrictions of the search content
5. **Privacy Protection**: Pay attention to the privacy of search content

## troubleshooting

### FAQ
1. **No results found**: Try different keyword combinations
2. **Failed to obtain web content**: Check network connection and target website status
3. **Slow search speed**: Reduce the number of search results or content length
4. **Cache problem**: Clear the search cache and search again

### Debugging method
1. Check whether the search keywords are correct
2. Verify network connection status
3. View session information to understand search status
4. Use the cache management function to troubleshoot problems

### Performance optimization
1. Set the number of search results appropriately
2. Get web content as needed
3. Clean search cache regularly
4. Use session management to optimize the search process

Through search tools, you can quickly obtain various information on the Internet to support various needs in study, work and life.