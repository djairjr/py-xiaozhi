# Calendar Tools

The schedule management tool is a complete set of MCP schedule management tools that provides comprehensive schedule management functions such as schedule creation, query, update, and deletion.

### Common usage scenarios

**Create schedule:**
- "Help me arrange a meeting schedule for 10 o'clock tomorrow morning"
- "Remind me to have a meeting next Tuesday at 3pm"
- "Set up a stand-up meeting every morning at 9am"
- "Schedule an important meeting at 14:30 on July 15, 2025 and end at 16:00"

**Inquiry schedule:**
- "What are your plans for today?"
- "Tomorrow's schedule"
- "Meeting schedule for this week"
- "All schedules for next month"
- "What's coming up lately"

**Modify schedule:**
- "Change tomorrow's meeting to 2pm"
- "Meeting description changed to Team Discussion"
- "Extend meeting time to 3 hours"

**Delete schedule:**
- "Cancel tomorrow's meeting"
- "Delete all rest reminders for today"
- "Clear all schedules for this week"

**Category Management:**
- "View schedules for all work types"
- "Create a meeting category schedule"
- "What schedule categories are there?"

### Usage tips

1. **Natural description of time**: Supports natural language time expressions such as "tomorrow", "next Tuesday", "this afternoon", etc.
2. **Smart Duration**: If the end time is not specified, the system will intelligently set an appropriate duration based on the schedule type.
3. **Category Management**: You can set categories for the schedule, such as "work", "meeting", "rest", etc.
4. **Reminder function**: You can set the reminder how many minutes in advance, the default is 15 minutes
5. **Batch Operation**: Supports batch query and deletion of schedules

The AI ​​assistant will automatically select the appropriate schedule management tool based on your needs and provide you with convenient schedule management services.

## Function overview

### Core functions of schedule management
- **Schedule Creation**: Create schedule events with time, description, and classification
- **Schedule Query**: Query schedule by date, category, and time range
- **Schedule Update**: Modify the title, time, description and other information of the schedule
- **Schedule Delete**: Delete single or batch delete schedule events

### Time management function
- **Smart Duration**: Automatically set the appropriate duration according to the schedule type
- **Upcoming**: Query the schedule within the specified time in the future
- **Reminder Settings**: Configurable advance reminder time
- **Time conflict detection**: Prevent the creation of schedules with time conflicts

### Classification management
- **Category Statistics**: View all used schedule categories
- **Query by Category**: Filter schedules by category
- **Intelligent Classification**: The system automatically assigns appropriate classifications to common activities

## Tool list

### 1. Schedule creation tool

#### create_event - Create a schedule event
Create a new calendar event.

**parameter:**
- `title` (required): schedule title
- `start_time` (required): start time, ISO format "2025-07-09T10:00:00"
- `end_time` (optional): end time, if not provided, it will be set intelligently
- `description` (optional): schedule description
- `category` (optional): schedule category, default is "default"
- `reminder_minutes` (optional): number of minutes to remind in advance, default 15 minutes

**Usage scenario:**
- Arrange meetings
- Set reminders
- Create work tasks
- Arrange personal events

### 2. Schedule query tool

#### get_events_by_date - Query schedule by date
Query schedule events within a specified date range.

**parameter:**
- `date_type` (optional): query type, supports "today", "tomorrow", "week", "month"
- `category` (optional): filter by category
- `start_date` (optional): Custom start date
- `end_date` (optional): Custom end date

**Usage scenario:**
- Check today's schedule
- Check out this week's schedule
- View schedule by category
- Customized time range query

#### get_upcoming_events - Get upcoming events
Query the upcoming schedule within a specified time in the future.

**parameter:**
- `hours` (optional): Query the schedule within the next few hours, the default is 24 hours

**Usage scenario:**
- Check out what's next
- Schedule reminder
- time planning

### 3. Schedule update tool

#### update_event - Update schedule event
Modify existing schedule event information.

**parameter:**
- `event_id` (required): schedule event ID
- `title` (optional): new schedule title
- `start_time` (optional): new start time
- `end_time` (optional): new end time
- `description` (optional): new schedule description
- `category` (optional): new schedule category
- `reminder_minutes` (optional): new reminder time

**Usage scenario:**
- Modify meeting time
- Update schedule description
- Adjust reminder time
- Change schedule category

### 4. Schedule deletion tool

#### delete_event - delete schedule event
Delete the specified calendar event.

**parameter:**
- `event_id` (required): ID of the calendar event to be deleted

**Usage scenario:**
- Cancel meeting
- Delete expired schedule
- Clean up unnecessary events

#### delete_events_batch - Batch delete schedules
Delete eligible calendar events in batches.

**parameter:**
- `date_type` (optional): delete type, supports "today", "tomorrow", "week", "month"
- `start_date` (optional): Custom start date
- `end_date` (optional): Custom end date
- `category` (optional): delete by category
- `delete_all` (optional): whether to delete all schedules

**Usage scenario:**
- Clear the schedule for a certain day
- Delete all schedules of a certain category
- Batch cleanup of expired schedules

### 5. Category management tools

#### get_categories - Get schedule categories
Get all used schedule categories.

**parameter:**
none

**Usage scenario:**
- View all categories
- Classification statistics
- Classification management

## Usage example

### Schedule creation example

```python
# Create a simple schedule
result = await mcp_server.call_tool("create_event", {
"title": "Team Meeting",
    "start_time": "2025-07-15T14:00:00",
    "end_time": "2025-07-15T15:00:00",
"description": "Discuss project progress",
"category": "Conference"
})

# Create a schedule with smart duration
result = await mcp_server.call_tool("create_event", {
"title": "Stand-up meeting",
    "start_time": "2025-07-15T09:00:00",
"category": "Conference",
    "reminder_minutes": 10
})
```

### Schedule query example

```python
# Check today’s schedule
result = await mcp_server.call_tool("get_events_by_date", {
    "date_type": "today"
})

# Query this week’s meetings
result = await mcp_server.call_tool("get_events_by_date", {
    "date_type": "week",
"category": "Conference"
})

# Query the schedule for the next 12 hours
result = await mcp_server.call_tool("get_upcoming_events", {
    "hours": 12
})

# Custom time range query
result = await mcp_server.call_tool("get_events_by_date", {
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-01-31T23:59:59"
})
```

### Schedule update example

```python
# Update schedule time
result = await mcp_server.call_tool("update_event", {
    "event_id": "event-123",
    "start_time": "2025-07-15T15:00:00",
    "end_time": "2025-07-15T16:00:00"
})

# Update schedule description
result = await mcp_server.call_tool("update_event", {
    "event_id": "event-123",
"description": "Updated meeting description",
    "reminder_minutes": 30
})
```

### Schedule deletion example

```python
# Delete a single schedule
result = await mcp_server.call_tool("delete_event", {
    "event_id": "event-123"
})

# Delete all schedules today
result = await mcp_server.call_tool("delete_events_batch", {
    "date_type": "today"
})

# Delete schedules of specific categories
result = await mcp_server.call_tool("delete_events_batch", {
"category": "rest",
    "date_type": "week"
})
```

### Classification management example

```python
# Get all categories
result = await mcp_server.call_tool("get_categories", {})
```

## Data structure

### Calendar Event (CalendarEvent)
```python
@dataclass
class CalendarEvent:
id: str # event ID
title: str # Schedule title
start_time: str #Start time (ISO format)
end_time: str # End time (ISO format)
description: str # Schedule description
category: str #Schedule classification
reminder_minutes: int # Reminder time (minutes)
reminder_time: str # Reminder time (ISO format)
reminder_sent: bool # Whether a reminder has been sent
created_at: str # Creation time
updated_at: str # Update time
```

### Query result format
```python
{
    "success": true,
    "date_type": "today",
    "total_events": 3,
    "events": [
        {
            "id": "event-123",
"title": "Team Meeting",
            "start_time": "2025-07-15T14:00:00",
            "end_time": "2025-07-15T15:00:00",
"description": "Discuss project progress",
"category": "Conference",
            "display_time": "01/15 14:00 - 15:00",
            "reminder_minutes": 15
        }
    ]
}
```

## Intelligent functions

### Intelligent duration setting
The system will automatically set the appropriate duration based on the schedule type:
- **Short activity** (reminder, rest, standing): 5 minutes
- **Work related** (meetings, work): 1 hour
- **Judge based on the title**: short-term activities containing keywords such as "reminder" and "rest"
- **Default**: 30 minutes

### Time expression analysis
Supports multiple time formats:
- ISO standard format: `2025-07-15T14:00:00`
- Relative time: today, tomorrow, next week, etc.
- Natural language: 10 a.m., 3 p.m., etc.

### Classification intelligent recognition
The system can automatically identify appropriate categories based on schedule content:
- Contains the keyword "meeting" → Conference classification
- Contains the keyword "rest" → Rest classification
- Contains the "job" keyword → Job classification

## Best Practices

### 1. Time format specification
- Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`
- Ensure time accuracy, including time zone information
- End time should be later than start time

### 2. Classification management
- Use consistent category naming
- Create meaningful category names
- Regularly clean up categories that are no longer used

### 3. Reminder settings
- Set appropriate reminder time according to the importance of the schedule
- It is recommended to remind important meetings 30 minutes or earlier in advance
- Daily reminders can be set for a shorter time

### 4. Schedule planning
- Reasonably arrange the time between schedules
- Avoid an overly tight schedule
- Review and adjust schedule regularly

## Notes

1. **Time Conflict**: The system will detect time conflicts and it is recommended to avoid overlapping schedules
2. **Time zone handling**: Ensure that the time format contains correct time zone information
3. **Data Persistence**: Schedule data will be automatically saved to the local database
4. **Performance considerations**: Pay attention to the size of the data when performing batch operations.

## troubleshooting

### FAQ
1. **Time format error**: Make sure to use the correct ISO format
2. **Event does not exist**: Check whether the event ID is correct
3. **Time Conflict**: Adjust time or delete conflicting schedule
4. **Classification problem**: Check whether the classification name is correct

### Debugging method
1. Check the time parameter format
2. Verify the validity of the event ID
3. View the returned error message
4. Use query tools to verify data status

With schedule management tools, you can easily manage personal and team schedules and improve time management efficiency.
