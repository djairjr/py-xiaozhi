# Home Assistant MCP Integration

To improve architectural flexibility and stability, py-xiaozhi has removed the built-in Home Assistant (HA). You can now access HA through the WSS-based Home Assistant MCP plug-in, and directly connect to the Xiaozhi AI server through the MCP protocol without any transfer. This plug-in is maintained by c1pher-cn as an open source and fully supports device status query, entity control and automated management.

Project address: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi)

## Plug-in features

### Core Competencies

1. **Direct connection to Xiaozhi server**: Home Assistant, as an MCP server, directly connects to Xiaozhi server through WebSocket protocol without any transfer.
2. **Multiple API Group Agent**: Select multiple API groups in one entity at the same time (Home Assistant comes with its own control API, user-defined MCP Server)
3. **Multi-entity support**: Supports configuring multiple entity instances at the same time
4. **HACS integration**: One-click installation through HACS store for easy management and updates

### Technical advantages

- **Low Latency**: Direct connection architecture to reduce network transit delay
- **High Reliability**: Based on WebSocket long connection, better stability
- **Easy to Expand**: Supports proxying for other MCP Servers, with strong scalability
- **Easy to maintain**: HACS management, automatic updates

## Common usage scenarios

**Equipment status query:**

- "What is the current status of the living room lights?"
- "View status of all lights"
- "How many degrees does the temperature sensor display?"
- "Is the air conditioner on now?"

**Device Control:**

- "Turn on the living room light"
- "Turn off all lights"
- "Set the air conditioner temperature to 25 degrees"
- "Adjust the brightness of the living room lights to 80%"

**Scene Control:**

- "Enable sleep mode"
- "Activate home scene"
- "Perform Good Night Scene"
- "Start party mode"

**Advanced Controls:**

- "Control TV via script"
- "Execute custom automation"
- "Control multimedia devices"
- "Manage Security Systems"

## Installation Guide

### Prerequisites

- Home Assistant is installed and running
- HACS (Home Assistant Community Store) installed
- Xiaozhi AI account and MCP access point address

### Installation steps

#### 1. Install via HACS

1. Open HACS and search for `xiaozhi` or `ha-mcp-for-xiaozhi`

<img width="700" alt="HACS search interface" src="https://github.com/user-attachments/assets/fa49ee7c-b503-49fa-ad63-512499fa3885" />

2. Click to download and install the plug-in

<img width="500" alt="Plug-in download interface" src="https://github.com/user-attachments/assets/1ee75d6f-e1b0-4073-a2c7-ee0d72d002ca" />

3. Restart Home Assistant

#### 2. Manual installation

If you cannot install via HACS, you can download it manually:

1. Download the latest version from [GitHub Releases](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/releases)
2. Unzip to the `custom_components` directory
3. Restart Home Assistant

### Configuration steps

#### 1. Add integration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for "Mcp" or "MCP Server for Xiaozhi"

<img width="600" alt="Add integrated interface" src="https://github.com/user-attachments/assets/07a70fe1-8c6e-4679-84df-1ea05114b271" />

3. Select and click Add

#### 2. Configuration parameters

The configuration interface requires filling in the following information:

**Basic configuration:**

- **Xiaozhi MCP access point address**: MCP access address obtained from Xiaozhi AI background
- **Device Name**: Set an identifying name for this Home Assistant instance

**API group selection:**

- **Assist**: Home Assistant’s built-in control function
- **Other MCP Server**: If you have configured other MCP servers in Home Assistant, you can choose to proxy them to Xiaozhi as well.

<img width="600" alt="Configuration interface" src="https://github.com/user-attachments/assets/38e98fde-8a6c-4434-932c-840c25dc6e28" />

#### 3. Entity public settings

In order for Xiaozhi to control the device, the corresponding entity needs to be exposed:

1. Go to **Settings > Voice Assistant > Public**
2. Select the devices and entities that need to be controlled by Xiaozhi
3. Save settings

#### 4. Verify connection

1. Wait about 1 minute after the configuration is completed.
2. Log in to the Xiaozhi AI backend and enter the MCP access point page.
3. Click Refresh to check whether the connection status is normal.

<img width="600" alt="Connection status check" src="https://github.com/user-attachments/assets/ace79a44-6197-4e94-8c49-ab9048ed4502" />

## Usage example

### Basic device control

```
User: "Turn on the living room lights"
Xiaozhi: "Okay, I've turned on the living room light for you."

User: "Adjust the air conditioner temperature to 26 degrees"
Xiaozhi: "The air conditioner temperature has been set to 26 degrees"

User: "Turn off all lights"
Xiaozhi: "All lights have been turned off for you"
```

### Status Query

```
User: "What is the current temperature in the living room?"
Xiaozhi: "The temperature sensor in the living room shows that the current temperature is 23.5 degrees"

User: "Which lights are on now?"
Xiaozhi: "The lights currently turned on are: living room lamp, bedroom bedside lamp"
```

### Scene control

```
User: "Execute sleep mode"
Xiaozhi: "The sleep mode scene has been executed for you, all lights have been turned off, and the curtains have been drawn."

User: "Enable home scene"
Xiaozhi: "Welcome home! The living room lights and entrance lights have been turned on for you, and the air conditioner has been adjusted to a comfortable temperature."
```

## Debugging instructions

### 1. Entity exposure check

The number of tools exposed depends on the kind of entities you expose to Home Assistant:

- Go to **Settings > Voice Assistant > Public**
- Make sure the device you need to control has been added to the public list

### 2. Version requirements

It is recommended to use the latest version of Home Assistant:

- The tools and API provided by the new version are more complete
- The May version has significant improvements in tool support compared to the March version

### 3. Debugging method

When the control effect does not meet expectations:

**View Xiaozhi’s chat history:**

1. Check how Xiaozhi understands and processes commands
2. Confirm whether the Home Assistant tool is called
3. Analyze whether the calling parameters are correct

**Known issues:**

- Lighting controls may conflict with built-in screen controls
- Music controls may conflict with built-in music functionality
- These issues will be resolved next month after Xiaozhi server supports built-in tool selection

### 4. Debug log

If the Home Assistant function is called correctly but executes abnormally:

1. Turn on the debugging log of this plug-in in Home Assistant
2. Reproduce the problem operation
3. Check the detailed execution status in the log

## Demo video

To better understand the plugin functionality, you can watch the following demo video:

- [Access to demo video](https://www.bilibili.com/video/BV1XdjJzeEwe) - Basic installation and configuration process
- [Control TV Demo](https://www.bilibili.com/video/BV18DM8zuEYV) - TV control through custom script
- [Advanced Tutorial](https://www.bilibili.com/video/BV1SruXzqEW5) - Detailed tutorials for Home Assistant, LLM, MCP, and Xiaozhi

## troubleshooting

### FAQ

**1. Connection failed**

- Check whether the Xiaozhi MCP access point address is correct
- Confirm that the Home Assistant network connection is normal
- Check firewall settings

**2. The device cannot be controlled**

- Confirm that the device is exposed in the voice assistant
- Check whether the device entity status is normal
- Verify that the device supports the corresponding operation

**3. Some functional conflicts**

- Temporarily disable built-in features
- Adjust device naming to avoid conflicts
- Waiting for the update of Xiaozhi server tool selection function

**4. Response delay**

- Check network connection quality
- Optimize Home Assistant performance
- Reduce unnecessary entity disclosure

### Debugging Tips

1. Enable verbose logging
2. Test basic functions step by step
3. Compare normal working device configurations
4. Refer to community discussions and issues

## Community Support

### Project link

- **GitHub repository**: [ha-mcp-for-xiaozhi](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi)
- **Issue Feedback**: [GitHub Issues](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/issues)
- **Feature Request**: [GitHub Discussions](https://github.com/c1pher-cn/ha-mcp-for-xiaozhi/discussions)
