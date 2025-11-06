# System Tools

System tools are a comprehensive MCP system management toolset that provide system status monitoring, volume control, device management and other functions.

### Common usage scenarios

**System status query:**
- "View system status"
- "How is the system running now?"
- "Check device status"
- "Is there any problem with the system?"

**Volume Control:**
- "Turn the volume to 50"
- "Turn up the volume a little louder"
- "Set volume to 80"
- "What is the volume now?"

**Device Management:**
- "How many IoT devices are connected"
- "What is the device connection status?"
- "View device list"
- "Is the device working properly?"

**Application Status:**
- "What is the current status of the application"
- "Is the system busy?"
- "What is the current working mode"
- "Is the application running normally?"

### Usage tips

1. **System Monitoring**: Regularly check the system status to understand the health status of the equipment
2. **Volume Adjustment**: You can accurately set the volume value or use relative adjustment
3. **Device Check**: Pay attention to the connection status and number of IoT devices
4. **Status Understanding**: Understand the meaning of different device states

The AI ​​assistant will automatically call system tools based on your needs to provide you with system management and monitoring services.

## Function overview

### System status monitoring
- **Complete Status**: Get the complete running status of the system
- **Audio Status**: Monitor audio device and volume status
- **Application Status**: View application running status
- **Device Statistics**: Statistics of IoT device connection status

### Volume control function
- **Volume Settings**: Accurately set system volume
- **Volume Query**: Get the current volume level
- **Silence Detection**: Detect whether the system is in silent state
- **Audio Device**: Check audio device availability

### Device management function
- **Equipment Status**: Monitor the running status of the equipment
- **IoT Device**: Manage IoT device connections
- **Device Count**: Count the number of connected devices
- **Status Switch**: Track device status changes

### Application monitoring function
- **Application Status**: Monitor application status
- **Working Mode**: Identify the current working mode
- **Resource Usage**: Monitor resource usage
- **Error Handling**: Detect and report system errors

## Tool list

### 1. System status tool

#### get_system_status - Get system status
Get complete system operating status information.

**parameter:**
none

**Usage scenario:**
- System health check
- Troubleshooting
- Status monitoring
- Performance evaluation

**Return information:**
- Audio device status
- Application status
- IoT device statistics
- System error messages

### 2. Volume control tool

#### set_volume - Set the volume
Set the system volume to a specified level.

**parameter:**
- `volume` (required): volume level, range 0-100

**Usage scenario:**
- Volume adjustment
- Audio control
- Adaptation to the environment
- User preferences

**characteristic:**
- Volume range verification
- Dependency checking
- Asynchronous execution
- error handling

## Usage example

### System status query example

```python
# Get complete system status
result = await mcp_server.call_tool("get_system_status", {})
```

### Volume control example

```python
# Set volume to 50
result = await mcp_server.call_tool("set_volume", {
    "volume": 50
})

#Set the volume to maximum
result = await mcp_server.call_tool("set_volume", {
    "volume": 100
})

#Set the volume to minimum (mute)
result = await mcp_server.call_tool("set_volume", {
    "volume": 0
})
```

## Data structure

### System Status (SystemStatus)
```python
{
    "audio_speaker": {
        "volume": 75,
        "muted": false,
        "available": true
    },
    "application": {
        "device_state": "IDLE",
        "iot_devices": 3
    },
    "cpu_usage": 25.5,
    "memory_usage": 60.2,
    "disk_usage": 45.8,
    "network_status": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Audio Status (AudioStatus)
```python
{
    "volume": 75,
    "muted": false,
    "available": true,
"device_name": "Default speaker",
    "sample_rate": 44100,
    "channels": 2
}
```

### Application Status (ApplicationStatus)
```python
{
    "device_state": "IDLE",
    "iot_devices": 3,
"uptime": "2 hours and 30 minutes",
    "last_activity": "2024-01-15T10:28:00Z",
    "active_tasks": 2
}
```

### Error status (ErrorStatus)
```python
{
"error": "Volume control dependency is incomplete",
    "audio_speaker": {
        "volume": 50,
        "muted": false,
        "available": false,
        "reason": "Dependencies not available"
    },
    "application": {
        "device_state": "unknown",
        "iot_devices": 0
    }
}
```

## Device status description

### Application status type
- **IDLE**: Idle state, waiting for user input
- **LISTENING**: Listening for voice input
- **SPEAKING**: Playing voice output
- **CONNECTING**: Connecting to service
- **PROCESSING**: Request is being processed
- **ERROR**: An error condition occurred

### Audio device status
- **available**: The audio device is available
- **volume**: current volume level (0-100)
- **muted**: Whether it is in muted state
- **device_name**: audio device name

### IoT device status
- **connected**: Number of connected devices
- **device_types**: device type statistics
- **last_update**: last update time
- **health_status**: Device health status

## System monitoring indicators

### Performance indicators
- **CPU Usage**: System CPU usage percentage
- **Memory Usage**: System memory usage percentage
- **Disk Usage**: Percentage of disk space occupied
- **Network Status**: Network connection status

### Application indicators
- **Running Time**: How long the application has been running
- **Active Tasks**: Current number of active tasks
- **Last Activity**: Last activity time
- **Error Count**: Number of times errors occurred

### Equipment indicators
- **Connected Devices**: Number of connected IoT devices
- **Equipment Type**: Statistics of different types of equipment
- **Device Health**: Equipment health status assessment
- **Connection Quality**: Evaluation of device connection quality

## Volume control mechanism

### Volume setting process
1. **Parameter verification**: Verify the volume value range (0-100)
2. **Dependency Check**: Check whether the volume control dependency is available
3. **Asynchronous execution**: Execute volume setting in thread pool
4. **Status Update**: Update system volume status
5. **result return**: return the setting result

### Cross-platform support
- **Windows**: Use WASAPI interface
- **macOS**: Use CoreAudio framework
- **Linux**: Use ALSA/PulseAudio
- **Dependency Management**: Automatically detect and load platform dependencies

### Error handling
- **Missing Dependencies**: Detect and report missing dependencies
- **Permissions Issue**: Handle insufficient permissions
- **Device Unavailable**: Handles the case where the audio device is unavailable
- **Parameter Error**: Verify and handle parameter errors

## Best Practices

### 1. System monitoring
- Regularly check system status
- Pay attention to changes in performance indicators
- Handle error status promptly
- Monitor device connection status

### 2. Volume management
- Set appropriate volume level
- Consider usage environment and time
- Regularly check audio device status
- Handle audio device failures

### 3. Device Management
- Monitor IoT device connections
- Regularly check device health status
- Handle device connection issues
- Optimize device performance

### 4. Error handling
- Respond promptly to error status
- Analyze the cause of the error
- Implement recovery measures
- Record error log

## troubleshooting

### FAQ
1. **Volume setting failed**: Check the audio device and dependencies
2. **Abnormal system status**: Check application status
3. **Device connection problem**: Check IoT device connection
4. **Insufficient permissions**: Check system permission settings

### Debugging method
1. Check the system status for detailed information
2. Check error logs and error messages
3. Verify dependencies and permission settings
4. Test audio device functionality

### Performance optimization
1. Clean the system cache regularly
2. Optimize IoT device connection
3. Monitor resource usage
4. Adjust system parameter settings

## Security considerations

### Permission management
- Volume control requires appropriate permissions
- System status access control
- Device management permission verification
- User operation permission check

### Data Protection
- System status information sensitivity
- Device information privacy protection
- Safe storage of operation logs
- Error information desensitization processing

### Access control
- Restrict access to system functions
- Verify user identity
- Control operating permissions
- Audit operation records

System tools allow you to effectively monitor and manage system status to ensure normal operation and optimal performance of your equipment.