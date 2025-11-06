<p align="center" class="trendshift">
  <a href="https://trendshift.io/repositories/14130" target="_blank">
    <img src="https://trendshift.io/api/badge/repositories/14130" alt="Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/>
  </a>
</p>
<p align="center">
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/v/release/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github&color=blue" alt="Release"/>
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License: MIT"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/stargazers">
    <img src="https://img.shields.io/github/stars/huangjunsen0406/py-xiaozhi?style=flat-square&logo=github" alt="Stars"/>
  </a>
  <a href="https://github.com/huangjunsen0406/py-xiaozhi/releases/latest">
    <img src="https://img.shields.io/github/downloads/huangjunsen0406/py-xiaozhi/total?style=flat-square&logo=github&color=52c41a1&maxAge=86400" alt="Download"/>
  </a>
  <a href="https://gitee.com/huang-jun-sen/py-xiaozhi">
    <img src="https://img.shields.io/badge/Gitee-FF5722?style=flat-square&logo=gitee" alt="Gitee"/>
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/guide/00_%E6%96%87%E6%A1%A3%E7%9B%AE%E5%BD%95.html">
<img alt="Usage Documentation" src="https://img.shields.io/badge/Usage Documentation-Click to view-blue?labelColor=2d2d2d" />
  </a>
</p>

Simplified Chinese | [English](README.en.md)

## Project Introduction

py-xiaozhi is a Xiaozhi voice client implemented in Python, designed to learn through code and experience the AI ​​Xiaozhi voice function without hardware conditions.
This warehouse is transplanted based on [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)

## Demo

- [Bilibili Demonstration Video](https://www.bilibili.com/video/BV1HmPjeSED2/#reply255921347937)

![Image](./documents/docs/guide/images/system interface.png)

## Features

### 🎯Core AI functions

- **AI Voice Interaction**: Supports voice input and recognition, realizes intelligent human-computer interaction, and provides a natural and smooth conversation experience
- **Visual multi-modal**: supports image recognition and processing, provides multi-modal interaction capabilities, and understands image content
- **Smart Wake**: Supports multiple wake word activation interactions, eliminating the trouble of manual operation (can be configured to turn on)
- **Automatic dialogue mode**: achieve continuous dialogue experience and improve user interaction fluency

### 🔧 MCP Tool Ecosystem

- **System control tools**: system status monitoring, application management, volume control, device management, etc.
- **Schedule Management Tool**: Full-featured schedule management, supports creation, query, update, delete events, intelligent classification and reminders
- **Scheduled task tool**: countdown timer function, supports delayed execution of MCP tools, and multi-task parallel management
- **Music player tool**: Online music search and playback, supports playback control, lyrics display, and local cache management
- **12306 Query Tool**: 12306 railway ticket query, supports ticket query, transfer query, train route query
- **Search tool**: Internet search and web content acquisition, supports Bing search and intelligent content analysis
- **Recipe Tool**: Rich recipe library, supports recipe search, category query, and intelligent recommendation
- **Map Tools**: AMAP map service, supporting geocoding, route planning, surrounding search, and weather query
- **Bazi numerology tool**: Traditional horoscope numerology analysis, supports horoscope calculation, marriage analysis, almanac query
- **Camera Tool**: Image capture and AI analysis, supporting photo recognition and intelligent question and answer

### 🏠 IoT device integration

- **Device Management Architecture**: Unified device management based on Thing mode, supporting asynchronous calling of properties and methods
- **Smart Home Control**: Supports device control such as lights, volume, temperature sensors, etc.
- **Status synchronization mechanism**: real-time status monitoring, supports incremental updates and concurrent status acquisition
- **Extensible Design**: Modular device driver, easy to add new device types

### 🎵 Advanced audio processing

- **Multi-level audio processing**: Support Opus codec, real-time resampling
- **Voice Activity Detection**: VAD detector implements intelligent interruption and supports real-time monitoring of voice activities
- **Wake Word Detection**: Offline speech recognition based on Sherpa-ONNX, supports multiple wake words and pinyin matching
- **Audio stream management**: independent input and output streams, supports stream reconstruction and error recovery
- **Audio Echo Cancellation**: Integrated WebRTC audio processing module to provide high-quality echo cancellation function
- **System Audio Recording**: Supports system audio recording and implements audio loopback processing

### 🖥️ User Interface

- **Graphic Interface**: Modern GUI based on PyQt5, supports Xiaozhi expressions and text display, enhancing the visual experience
- **Command line mode**: supports CLI operation, suitable for embedded devices or GUI-less environments
- **System Tray**: Background operation support, integrated system tray function
- **Global shortcut keys**: Support global shortcut key operations to improve ease of use.
- **Setting interface**: Complete settings management interface, supporting configuration customization

### 🔒 Security and stability

- **Encrypted Audio Transmission**: Supports WSS protocol to ensure the security of audio data and prevent information leakage
- **Device Activation System**: Supports v1/v2 dual-protocol activation, automatically processes verification codes and device fingerprints
- **Error Recovery**: Complete error handling and recovery mechanism, supports disconnection and reconnection

### 🌐 Cross-platform support

- **System Compatibility**: Compatible with Windows 10+, macOS 10.15+ and Linux systems
- **Protocol support**: Supports WebSocket and MQTT dual protocol communication
- **Multi-environment deployment**: Supports GUI and CLI dual modes to adapt to different deployment environments
- **Platform Optimization**: Audio and system control optimization for different platforms

### 🔧 Development friendly

- **Modular Architecture**: Clear code structure and separation of responsibilities to facilitate secondary development
- **Asynchronous First**: event-driven architecture based on asyncio, high-performance concurrent processing
- **Configuration Management**: Hierarchical configuration system, supporting dot notation access and dynamic updates
- **Logging System**: complete logging and debugging support
- **API Documentation**: Detailed code documentation and usage guide

## System requirements

### Basic requirements

- **Python version**: 3.9 - 3.12
- **Operating system**: Windows 10+, macOS 10.15+, Linux
- **Audio Devices**: microphone and speaker devices
- **Network Connection**: Stable Internet connection (for AI services and online features)

### Recommended configuration

- **Memory**: At least 4GB RAM (8GB+ recommended)
- **Processor**: modern CPU supporting AVX instruction set
- **Storage**: At least 2GB free disk space (for model files and cache)
- **Audio**: Audio devices that support 16kHz sampling rate

### Optional feature requirements

- **Voice wakeup**: Need to download the Sherpa-ONNX speech recognition model
- **Camera Features**: Requires camera device and OpenCV support

## Please look here first

- Read [Project Documentation](https://huangjunsen0406.github.io/py-xiaozhi/) carefully. The startup tutorial and file description are all in it.
- main is the latest code. Every time you update, you need to manually reinstall pip dependencies to prevent you from having them locally after I add dependencies.

[Using Xiaozhi client from scratch (video tutorial)](https://www.bilibili.com/video/BV1dWQhYEEmq/?vd_source=2065ec11f7577e7107a55bbdc3d12fce)

## Technical architecture

### Core architecture design

- **Event-driven architecture**: Asynchronous event loop based on asyncio, supporting high concurrency processing
- **Layered design**: clear separation of application layer, protocol layer, device layer and UI layer
- **Single case mode**: The core components adopt single case mode to ensure unified management of resources
- **Plug-in**: MCP tool system and IoT devices support plug-in extensions

### Key technical components

- **Audio processing**: Opus codec, WebRTC echo cancellation, real-time resampling, system audio recording
- **Speech recognition**: Sherpa-ONNX offline model, voice activity detection, wake word recognition
- **Protocol communication**: WebSocket/MQTT dual protocol support, encrypted transmission, automatic reconnection
- **Configuration system**: hierarchical configuration, dot notation access, dynamic update, JSON/YAML support

### Performance optimization

- **Asynchronous First**: System-wide asynchronous architecture to avoid blocking operations
- **Memory Management**: Intelligent caching, garbage collection
- **Audio Optimization**: 5ms low latency processing, queue management, streaming
- **Concurrency Control**: Task pool management, semaphore control, thread safety

### Security mechanism

- **Encrypted Communication**: WSS/TLS encryption, certificate verification
- **Device Authentication**: dual-protocol activation, device fingerprint recognition
- **Permission Control**: Tool permission management, API access control
- **Error isolation**: exception isolation, fault recovery, graceful degradation

## Development Guide

### Project structure

```
py-xiaozhi/
├── main.py # Main entrance of the application (CLI parameter processing)
├── src/
│ ├── application.py # Application core logic
│ ├── audio_codecs/ # Audio codecs
│ │ ├── aec_processor.py # Audio echo cancellation processor
│ │ ├── audio_codec.py # Audio codec basic class
│ │ └── system_audio_recorder.py # System audio recorder
│ ├── audio_processing/ # Audio processing module
│ │ ├── vad_detector.py # Voice activity detection
│ │ └── wake_word_detect.py # Wake word detection
│ ├── core/ # core component
│ │ ├── ota.py # Online update module
│ │ └── system_initializer.py # System initializer
│ ├── display/ # Display interface abstraction layer
│ ├── iot/ # IoT device management
│ │ ├── thing.py # Device base class
│ │ ├── thing_manager.py # Device Manager
│ │ └── things/ # Specific equipment implementation
│ ├── mcp/ # MCP tool system
│ │ ├── mcp_server.py # MCP server
│ │ └── tools/ # Various tool modules
│ ├── protocols/ # Communication protocol
│ ├── utils/ # Utility function
│ └── views/ # UI view component
├── libs/ # Third-party native library
│ ├── libopus/ # Opus audio codec library
│ ├── webrtc_apm/ # WebRTC audio processing module
│ └── SystemAudioRecorder/ # System audio recording tool
├── config/ # Configuration file directory
├── models/ # Speech model file
├── assets/ # Static resource files
├── scripts/ # Auxiliary script
├── requirements.txt # Python dependency package list
└── build.json # Build configuration file
```

### Development environment settings

```bash
# Clone project
git clone https://github.com/huangjunsen0406/py-xiaozhi.git
cd py-xiaozhi

# Install dependencies
pip install -r requirements.txt

# Code formatting
./format_code.sh

# Run the program - GUI mode (default)
python main.py

# Run the program - CLI mode
python main.py --mode cli

#Specify communication protocol
python main.py --protocol websocket # WebSocket (default)
python main.py --protocol mqtt # MQTT protocol
```

### Core development model

- **Asynchronous first**: Use `async/await` syntax to avoid blocking operations
- **Error Handling**: Complete exception handling and logging
- **Configuration Management**: Use `ConfigManager` to unify configuration access
- **Test-driven**: Write unit tests to ensure code quality

### Extension development

- **Add MCP tool**: Create a new tool module in the `src/mcp/tools/` directory
- **Add IoT device**: Inherit the `Thing` base class to implement new devices
- **Add protocol**: Implement `Protocol` abstract base class
- **Add interface**: Extend `BaseDisplay` to implement new UI components

### State flow diagram

```
                        +----------------+
                        |                |
                        v                |
+------+ wake word/button +------------+ | +------------+
| IDLE | -----------> | CONNECTING | --+-> | LISTENING  |
+------+              +------------+       +------------+
   ^                                            |
| | Voice recognition completed
   |          +------------+                    v
   +--------- |  SPEAKING  | <-----------------+
Finish playing +----------------+
```

## Contribution Guidelines

Issue reports and code contributions are welcome. Please make sure to follow these guidelines:

1. The coding style complies with the PEP8 specification
2. The PR submitted contains appropriate tests
3. Update related documents

## Community & Support

### Thanks to the following open source personnel
>
> Ranking in no particular order

[Xiaoxia](https://github.com/78)
[zhh827](https://github.com/zhh827)
[SiBo Zhilian-Li Honggang](https://github.com/SmartArduino)
[HonestQiao](https://github.com/HonestQiao)
[vonweller](https://github.com/vonweller)
[Sun Wei Gong](https://space.bilibili.com/416954647)
[isamu2025](https://github.com/isamu2025)
[Rain120](https://github.com/Rain120)
[kejily](https://github.com/kejily)
[电wavebilibilijun](https://space.bilibili.com/119751)
[Saibao Intelligence](https://shop115087494.m.taobao.com/?refer=https%3A%2F%2Fm.tb.cn%2F&ut_sk=1.WMelxbgDQWkDAJ1Rq9Pn7DCD_21380790_1757337352472.Copy.shop&suid=0E 25E948-651D-46E0-8E89-5C8CB03B4F56&shop_navi=shopindex&sourceType=shop&shareUniqueId=33038752403&un=d22c5ceda82844ab8bd7bab98ffeb263&share_crt_v=1& un_site=0&spm=a2159r.13376460.0.0&sp_tk=dkRKUjRKUWo2ZHY%3D&bc_fl_src=share-1041250486811064-2-1&cpp=1&shareurl=true&short_name=h.SaBKVHytsCKIPNS&bx sign=scdGtSe264e_qkFQBh0rXCkF-Mrb_s6t35EnpVBBU5dsrd-J24c-_rn_PhJiXRk0hg2hj GoAm0L7j2UQg27OIH_6gZkbhKDyLziD2cy4pDf8sC3KmqrF55TXP3USZaPTw_-&app=weixin)

### Sponsorship support

<div align="center">
<h3>Thanks to all sponsors for their support ❤️</h3>
<p>Whether it is interface resources, equipment compatibility testing or financial support, every help makes the project more complete</p>
  
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
<img src="https://img.shields.io/badge/View-Sponsor List-brightgreen?style=for-the-badge&logo=github" alt="Sponsor List">
  </a>
  <a href="https://huangjunsen0406.github.io/py-xiaozhi/sponsors/" target="_blank">
<img src="https://img.shields.io/badge/become-a-project-sponsor-orange?style=for-the-badge&logo=heart" alt="become a sponsor">
  </a>
</div>

## Project statistics

[![Star History Chart](https://api.star-history.com/svg?repos=huangjunsen0406/py-xiaozhi&type=Date)](https://www.star-history.com/#huangjunsen0406/py-xiaozhi&Date)

## License

[MIT License](LICENSE)
