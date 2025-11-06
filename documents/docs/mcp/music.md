#Music Tools

The music player tool is a feature-rich MCP music player that supports online search and playback, local music management, lyrics display and other functions.

### Common usage scenarios

**Search and play online music:**
- "Play Jay Chou's Blue and White Porcelain"
- "I want to listen to Deng Ziqi's songs"
- "Play some soft music"
- "Play the latest popular songs"

**Playback Controls:**
- "Pause music"
- "Continue playing"
- "Stop playing"
- "The music is halfway through"

**Local Music Management:**
- "View local music"
- "Play the local song"
- "Search Jay Chou in local music"

**Playing status query:**
- "What song is playing now?"
- "How is the playback progress?"
- "How long does this song last?"

**Lyrics function:**
- "Show lyrics"
- "What are the current lyrics"
- "Are there any lyrics?"

**Advanced Features:**
- "Jump to 1 minute 30 seconds"
- "Fast forward to the climax"
- "Back to the beginning"

### Usage tips

1. **Clear song information**: Providing song title, artist name or album name will help in more accurate search
2. **Network Connection**: Online search and playback require a stable network connection.
3. **Local Cache**: Played songs will be automatically cached and played faster next time
4. **Volume Control**: You can ask to adjust the volume or mute
5. **Lyrics Synchronization**: Supports real-time lyrics display to enhance the listening experience

The AI ​​assistant will automatically call music playback tools based on your needs to provide you with a smooth music experience.

## Function overview

### Online music function
- **Smart Search**: Supports multiple search methods such as song title, artist, album, etc.
- **High Quality Playback**: Support high quality audio streaming playback
- **Lyrics Display**: Real-time synchronized lyrics display
- **Auto Cache**: Played songs are automatically cached locally.

### Local music management
- **Local Scan**: Automatically scan local music files
- **Metadata Extraction**: Automatically extract song title, artist, album and other information
- **Format Support**: Supports MP3, M4A, FLAC, WAV, OGG and other formats
- **Smart Search**: Quickly search in local music

### Playback control function
- **Basic Controls**: Play, Pause, Stop
- **Progress Control**: Jump to the specified time position
- **Status Query**: Get playback status, progress and other information
- **Error Handling**: Complete error handling and recovery mechanism

### User experience features
- **UI Integration**: Seamless integration with application interface
- **Real-time feedback**: Display playback status and lyrics in real time
- **Smart Cache**: Optimize storage space usage
- **Background Play**: Supports continuous playback in the background

## Tool list

### 1. Online music tools

#### search_and_play - Search and play
Search online music and start playing.

**parameter:**
- `song_name` (required): the song name, artist or keyword to search for

**Usage scenario:**
- Play specified songs
- Search songs by singers
- Play popular music

### 2. Local music tools

#### get_local_playlist - Get the local music list
Get a list of locally cached music files.

**parameter:**
- `force_refresh` (optional): whether to force refresh, default false

**Usage scenario:**
- View local music
- Manage music library
- Select playlist

#### search_local_music - Search local music
Search for specified songs in local music.

**parameter:**
- `query` (required): search keyword

**Usage scenario:**
- Find local songs
- Artist search
- Album search

#### play_local_song_by_id - Play local songs
Play local music based on song ID.

**parameter:**
- `file_id` (required): local music file ID

**Usage scenario:**
- Play specified local songs
- Select from playlist
- Quickly play cached music

### 3. Playback control tool

#### play_pause - Play/pause switch
Switch play and pause state.

**parameter:**
none

**Usage scenario:**
- Pause current playback
- Resume playback
- Playback controls

#### stop - Stop playing
Stop current playback.

**parameter:**
none

**Usage scenario:**
- Stop playback completely
- End the music session
- Clear playback status

#### seek - jump to a specified location
Jump to the specified time position in the song.

**parameter:**
- `position` (required): jump position (seconds)

**Usage scenario:**
- Fast forward to the climax
- Play a segment repeatedly
- Skip the parts you don't like

### 4. Information query tool

#### get_status - Get playback status
Get detailed status information of the current player.

**parameter:**
none

**Usage scenario:**
- Check playback progress
- Check playback status
- Get song information

#### get_lyrics - Get lyrics
Get the lyrics of the currently playing song.

**parameter:**
none

**Usage scenario:**
- Show lyrics
- Sing-along songs
- Learn lyrics

## Usage example

### Online music playback example

```python
# Search and play songs
result = await mcp_server.call_tool("search_and_play", {
"song_name": "Jay Chou Blue and White Porcelain"
})

# Play/pause control
result = await mcp_server.call_tool("play_pause", {})

# Stop playing
result = await mcp_server.call_tool("stop", {})

# Jump to the specified location
result = await mcp_server.call_tool("seek", {
    "position": 90.5
})
```

### Local music management example

```python
# Get local music list
result = await mcp_server.call_tool("get_local_playlist", {
    "force_refresh": True
})

# Search local music
result = await mcp_server.call_tool("search_local_music", {
"query": "Jay Chou"
})

# Play local songs
result = await mcp_server.call_tool("play_local_song_by_id", {
    "file_id": "song_123"
})
```

### Status query example

```python
# Get playback status
result = await mcp_server.call_tool("get_status", {})

# Get lyrics
result = await mcp_server.call_tool("get_lyrics", {})
```

## Technical architecture

### Music player core
- **Single case mode**: Globally unique player instance
- **Asynchronous design**: supports asynchronous operations and does not block the main thread
- **Status Management**: Complete playback status management
- **Error Handling**: Robust error handling mechanism

### Audio processing
- **Pygame integration**: Use Pygame Mixer for audio playback
- **Format Support**: Supports multiple audio formats
- **Caching mechanism**: Intelligent caching strategy to reduce repeated downloads
- **Sound Quality Optimization**: High-quality audio playback

### Online service integration
- **API Interface**: Integrate online music search API
- **Download Management**: Asynchronous download and cache management
- **Lyrics Service**: Real-time lyrics acquisition and display
- **Network Optimization**: Network request optimization and retry mechanism

### Local music management
- **File Scanning**: Automatically scan local music files
- **Metadata Extraction**: Use the Mutagen library to extract music metadata
- **Index Creation**: Create an index of music files to improve search efficiency
- **Format Recognition**: Intelligent recognition of music file formats

## Data structure

### Play status information
```python
{
    "status": "success",
"current_song": "Blue and White Porcelain - Jay Chou",
    "is_playing": true,
    "paused": false,
    "duration": 237.5,
    "position": 89.2,
    "progress": 37.6,
    "has_lyrics": true
}
```

### Music Metadata
```python
{
    "file_id": "song_123",
"title": "Blue and white porcelain",
"artist": "Jay Chou",
"album": "I'm very busy",
    "duration": "03:57",
    "file_size": 5242880,
    "format": "mp3"
}
```

### Lyrics data
```python
{
    "status": "success",
    "lyrics": [
"[00:12] The plain embryo outlines the blue and white brush strokes, which become darker and lighter",
"[00:18] The peonies depicted on the bottle are just like your first makeup",
"[00:24] The sandalwood slowly passes through the window and I understand my thoughts."
    ]
}
```

## Configuration instructions

### Audio configuration
Audio playback related configuration:
```python
AudioConfig = {
    "OUTPUT_SAMPLE_RATE": 44100,
    "CHANNELS": 2,
    "BUFFER_SIZE": 1024
}
```

### Cache configuration
Cache directory configuration:
```python
cache_dir = Path(project_root) / "cache" / "music"
temp_cache_dir = cache_dir / "temp"
```

### API configuration
Online music service configuration:
```python
config = {
    "SEARCH_URL": "http://search.kuwo.cn/r.s",
    "PLAY_URL": "http://api.xiaodaokg.com/kuwo.php",
    "LYRIC_URL": "http://m.kuwo.cn/newh5/singles/songinfoandlrc"
}
```

## Supported audio formats

### Play format
- **MP3**: The most common audio format
- **M4A**: Apple audio format
- **FLAC**: lossless audio format
- **WAV**: uncompressed audio format
- **OGG**: Open source audio format

### Metadata support
- **ID3 v1/v2**: MP3 metadata standard
- **MP4**: M4A file metadata
- **Vorbis**: OGG file metadata
- **FLAC**: FLAC file metadata

## Best Practices

### 1. Search optimization
- Use specific song and artist names
- Avoid using keywords that are too vague
- Can include album name to increase accuracy

### 2. Cache management
- Clean unnecessary cache files regularly
- Monitor cache directory size
- Use force refresh to get the latest music list

### 3. Network optimization
- Make sure the network connection is stable
- Give priority to local music when the network is poor
- Set appropriate timeout

### 4. User experience
- Provide clear feedback on playback status
- Supports quick response control operations
- Handle playback errors gracefully

## troubleshooting

### FAQ
1. **Unable to search for songs**: Check network connection and API availability
2. **Playback failed**: Check audio device and file format
3. **Lyrics not displayed**: Check lyrics service and song ID
4. **Local music not displayed**: Check file permissions and format support

### Debugging method
1. Check the log output for detailed error information
2. Test network connection and API response
3. Verify audio file integrity
4. Check cache directory permissions

### Performance optimization
1. Properly set caching strategies
2. Optimize network request frequency
3. Use asynchronous operations to avoid blocking
4. Clean up temporary files regularly

Through music playback tools, you can enjoy a rich music experience, including online search, local playback, lyrics display and other functions.
