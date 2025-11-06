# Timer Tools

The timer tool is a powerful MCP countdown toolset that provides functions such as creation, management, and cancellation of scheduled tasks, and supports delayed execution of various operations.

### Common usage scenarios

**Regular reminder:**
- "Remind me to have a meeting in 5 minutes"
- "Remind me to take a break after 10 minutes"
- "Remind me to take medicine in half an hour"
- "Remind me to shut down my computer after 1 hour"

**Scheduled playback:**
- "Play music after 5 minutes"
- "Play my favorite song in 10 minutes"
- "Stop playing after 15 minutes"
- "Play alarm in 20 minutes"

**Timing system operation:**
- "Turn down the volume after 30 minutes"
- "Shut down the system after 1 hour"
- "Check system status after 10 minutes"
- "Check the weather in 5 minutes"

**Scheduled query:**
- "Check train tickets in 5 minutes"
- "Search news after 10 minutes"
- "Check schedule in 15 minutes"
- "Check the recipe in 20 minutes"

**Task Management:**
- "View current scheduled tasks"
- "Cancel the timer just set"
- "View all active timers"
- "Cancel reminder after 5 minutes"

### Usage tips

1. **Time expression**: Supports multiple time expressions, such as "5 minutes later", "half an hour later", "1 hour later"
2. **Task Description**: You can add a task description to help identify different scheduled tasks.
3. **Task Management**: You can view and cancel running scheduled tasks
4. **Flexible Settings**: Supports setting various types of delayed execution tasks

The AI ​​assistant will automatically call the timer tool according to your needs to provide you with convenient scheduled task management services.

## Function overview

### Countdown function
- **Scheduled execution**: Execute the task after delaying the specified time
- **Task Type**: Supports various MCP tool calls
- **Time Setting**: Flexible time setting options
- **Task Description**: Task description can be added for easy management

### Task management function
- **Task Creation**: Create a new scheduled task
- **Task Cancel**: Cancel the running scheduled task
- **Task Query**: View all active scheduled tasks
- **Status Monitoring**: Real-time monitoring of task execution status

###Execution control function
- **Delay Control**: Precisely control execution delay time
- **Task Queue**: Manage multiple concurrent scheduled tasks
- **Error handling**: Complete error handling mechanism
- **Logging**: Detailed task execution log

### System integration function
- **MCP Integration**: Seamless integration with other MCP tools
- **Asynchronous Execution**: Supports asynchronous task execution
- **Resource Management**: Reasonably manage system resources
- **Performance Optimization**: Optimize scheduled task performance

## Tool list

### 1. Scheduled task tool

#### start_countdown_timer - Start countdown task
Create and start a countdown task to perform the specified operation after the specified time.

**parameter:**
- `command` (required): MCP tool call to be executed, JSON format string
- `delay` (optional): delay time (seconds), default 5 seconds
- `description` (optional): task description

**Usage scenario:**
- Regular reminder
- Delay task execution
- Play music regularly
- Timing system operation

#### cancel_countdown_timer - Cancel the countdown task
Cancels the specified running countdown task.

**parameter:**
- `timer_id` (required): ID of the timer to be canceled

**Usage scenario:**
- Cancel unnecessary scheduled tasks
- Modify scheduled task settings
- Clean up scheduled tasks

#### get_active_countdown_timers - Get active timers
Get the status of all running countdown tasks.

**parameter:**
none

**Usage scenario:**
- View current scheduled tasks
- Manage scheduled tasks
- Monitor task status

## Usage example

### Scheduled task creation example

```python
# Create a reminder task after 5 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
"command": '{"name": "create_event", "arguments": {"title": "Meeting Reminder", "start_time": "2024-01-15T14:00:00"}}',
    "delay": 300,
"description": "Meeting Reminder"
})

#Create a task to play music after 10 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
"command": '{"name": "search_and_play", "arguments": {"song_name": "Light Music"}}',
    "delay": 600,
"description": "Play light music"
})

# Create a task to adjust the volume after 30 minutes
result = await mcp_server.call_tool("start_countdown_timer", {
    "command": '{"name": "set_volume", "arguments": {"volume": 30}}',
    "delay": 1800,
"description": "Turn down the volume"
})
```

### Task management example

```python
# View all active scheduled tasks
result = await mcp_server.call_tool("get_active_countdown_timers", {})

# Cancel the specified scheduled task
result = await mcp_server.call_tool("cancel_countdown_timer", {
    "timer_id": "timer_123"
})
```

## Data structure

### Countdown Task (CountdownTimer)
```python
{
    "timer_id": "timer_123",
    "command": {
        "name": "create_event",
        "arguments": {
"title": "Meeting Reminder",
            "start_time": "2024-01-15T14:00:00"
        }
    },
    "delay": 300,
"description": "Meeting Reminder",
    "created_at": "2024-01-15T10:25:00Z",
    "execute_at": "2024-01-15T10:30:00Z",
    "status": "running",
    "remaining_time": 240
}
```

### Task creation response (CreateResponse)
```python
{
    "success": true,
"message": "Countdown task created successfully",
    "timer_id": "timer_123",
    "execute_at": "2024-01-15T10:30:00Z",
    "remaining_time": 300,
"description": "Meeting Reminder"
}
```

### Task cancellation response (CancelResponse)
```python
{
    "success": true,
"message": "Countdown task has been cancelled",
    "timer_id": "timer_123",
    "cancelled_at": "2024-01-15T10:27:00Z"
}
```

### Active task list (ActiveTimers)
```python
{
    "success": true,
    "total_active_timers": 2,
    "timers": [
        {
            "timer_id": "timer_123",
"description": "Meeting Reminder",
            "remaining_time": 240,
            "execute_at": "2024-01-15T10:30:00Z",
            "status": "running"
        },
        {
            "timer_id": "timer_456",
"description": "Play music",
            "remaining_time": 480,
            "execute_at": "2024-01-15T10:33:00Z",
            "status": "running"
        }
    ]
}
```

## Task status description

### Task status type
- **running**: Running, waiting for execution
- **executing**: executing the task
- **completed**: execution completed
- **cancelled**: has been canceled
- **failed**: execution failed

### Time related fields
- **created_at**: task creation time
- **execute_at**: task execution time
- **remaining_time**: remaining time (seconds)
- **cancelled_at**: task cancellation time
- **completed_at**: task completion time

## Supported command types

### Schedule management commands
- **create_event**: Create a schedule event
- **update_event**: update schedule event
- **delete_event**: delete schedule event

### Music playback command
- **search_and_play**: Search and play music
- **play_pause**: Play/pause music
- **stop**: Stop playing
- **get_status**: Get playback status

### System control commands
- **set_volume**: Set volume
- **get_system_status**: Get system status

### Search query command
- **search_bing**: Internet search
- **query_train_tickets**: Query train tickets
- **get_recipe_by_id**: Get the recipe

## Time setting specifications

### Time unit
- **Seconds**: Minimum time unit
- **Minutes**: 60 seconds
- **Hours**: 3600 seconds
- **days**: 86400 seconds

### Common time settings
- **5 minutes**: 300 seconds
- **10 minutes**: 600 seconds
- **15 minutes**: 900 seconds
- **30 minutes**: 1800 seconds
- **1 hour**: 3600 seconds
- **2 hours**: 7200 seconds

### Time limit
- **MINIMUM DELAY**: 1 second
- **Maximum delay**: 24 hours (86400 seconds)
- **Recommended range**: 1 second - 4 hours

## Best Practices

### 1. Task design
- Use clear task descriptions
-Set a reasonable delay time
- Select the appropriate execution command
- Consider the timing of task execution

### 2. Task management
- Regularly check active tasks
- Cancel unnecessary tasks promptly
- Avoid creating too many concurrent tasks
- Arrange task time reasonably

### 3. Error handling
- Verify the correctness of the command format
- Handle task execution failure
- Monitor task execution status
- Record task execution log

### 4. Performance optimization
- Avoid creating tasks with too short intervals
- Reasonably control the number of concurrent tasks
- Optimize task execution logic
- Regularly clean up completed tasks

## Usage scenario example

### Work efficiency scenario
1. **Pomodoro Technique**: Reminder to take a break after 25 minutes
2. **Meeting Reminder**: Reminder preparation 5 minutes before the meeting
3. **Task switching**: Switch to the next task after 1 hour
4. **Scheduled Check**: Check emails every 30 minutes

### Life Assistant Scene
1. **Cooking timer**: Reminder to check the stove after 10 minutes
2. **Medication Reminder**: Reminder to take medication every 8 hours
3. **Exercise Reminder**: Reminder to get up and move every hour
4. **Sleep Reminder**: Remind you to get ready for bed at 10pm

### Entertainment scene
1. **Music Play**: Play bedtime music after 30 minutes
2. **Game Reminder**: Reminder to take a break after 1 hour
3. **Video Timing**: Pause the video after 2 hours
4. **Reading Reminder**: Remind to rest your eyes after 45 minutes

## Notes

1. **Time Accuracy**: The timer is based on system time to ensure that the system time is accurate
2. **Task Complexity**: Avoid performing overly complex operations in scheduled tasks
3. **Resource Management**: Reasonably control the number of concurrent tasks to avoid excessive resource occupation
4. **Error recovery**: The system will automatically clean up when task execution fails.
5. **Task Persistence**: Scheduled tasks will be lost after the system is restarted.

## troubleshooting

### FAQ
1. **Task creation failed**: Check command format and parameters
2. **Task execution failed**: Check whether the target tool is available
3. **Task cancellation failed**: Confirm whether the task ID is correct
4. **Time setting error**: Verify time parameter range

### Debugging method
1. Check the error information returned by task creation
2. Check the active task list to confirm task status
3. Verify whether the command format is correct
4. Test whether the target tool is working properly

### Performance optimization suggestions
1. Avoid creating too many short-interval tasks
2. Set task descriptions appropriately to facilitate management
3. Clean up unnecessary tasks regularly
4. Monitor system resource usage

Through the timer tool, you can easily set various scheduled tasks to improve work efficiency and life convenience.