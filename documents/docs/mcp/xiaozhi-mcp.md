# Xiaozhi MCP plug-in access guide

This document describes how to connect external MCP services to the Xiaozhi system to achieve function expansion and third-party tool integration.

## Overview

In addition to the built-in MCP tools, the Xiaozhi system also supports access to external MCP servers to achieve:
- Third-party tool integration
-Remote service call
- Distributed tool deployment
- Community tool sharing

## Architecture description

### Plug-in MCP architecture
```
Xiaozhi AI platform xiaozhi-mcphub external MCP server third-party tool
┌─────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────┐
│             │   │                 │   │                 │   │             │
│ MCP Client │◄──┤ MCP Server/Agent │◄──┤ MCP Server │◄──┤ Actual Tools │
│             │   │                 │   │                 │   │             │
└─────────────┘   └─────────────────┘   └─────────────────┘   └─────────────┘
```

### Connection method
1. **Standard Input and Output (stdio)**: Start the child process and conduct inter-process communication through the stdin/stdout pipe. It is suitable for local CLI tools such as Playwright, Amap, etc.
2. **Server Push Event (SSE)**: Event stream communication based on HTTP long connection, providing real-time two-way communication capabilities similar to WebSocket
3. **Streamable-http)**: TCP-based HTTP protocol encapsulation, supports streaming data transmission, and is suitable for remote API services and microservices
4. **OpenAPI**: Based on the connection method of the standard REST API specification, it automatically parses the OpenAPI specification and generates tool interfaces, suitable for standardized third-party API services.

## Related open source projects
Xiaozhi client project developed by the community, providing access methods for different platforms

### xiaozhi-mcphub (supported by this project)

**Xiaozhi MCP Hub** is an intelligent MCP tool bridge system optimized for Xiaozhi AI platform. It is developed based on the excellent MCPHub project and adds Xiaozhi platform integration and smart tool synchronization functions.

- **Project address**: [xiaozhi-mcphub](https://huangjunsen0406.github.io/xiaozhi-mcphub/)
- **GitHub**: [xiaozhi-mcphub](https://github.com/huangjunsen0406/xiaozhi-mcphub)
- **Core Features**:
- **Xiaozhi AI platform integration**: WebSocket automatic tool synchronization, real-time status update, protocol bridging
- **Enhanced MCP Management**: Supports stdio, SSE, HTTP protocols, hot-swappable configuration, centralized console
- **Smart Tool Routing**: Vector-based smart tool search and group management
- **Security authentication mechanism**: JWT+bcrypt user management, role permission control
- **Built-in mcp store**: Multiple mcp tools can be installed online without restarting and support hot updates
  
### xiaozhi-client
- **Project address**: [xiaozhi-client](https://github.com/shenjingnan/xiaozhi-client)
- **Function**: Xiaozhi AI client, specially used for MCP docking and aggregation
- **Core Features**:
- **Multiple access point support**: Multiple Xiaozhi access points can be configured to enable multiple devices to share one MCP configuration
- **MCP Server Aggregation**: Aggregate multiple MCP Servers through standard methods for unified management
- **Dynamic Tool Control**: Control the visibility of MCP Server tools to avoid abnormalities caused by too many tools
- **Multiple integration methods**: Supports integration into clients such as Cursor/Cherry Studio as a common MCP Server
- **Web Visual Configuration**: Modern Web UI interface, supports remote configuration and management
- **ModelScope integration**: Supports remote MCP services hosted by ModelScope

### HyperChat
- **Project address**: [HyperChat](https://github.com/BigSweetPotatoStudio/HyperChat)
- **Function**: Next generation AI workspace, the first multi-platform intelligent collaboration platform with the concept of "AI as Code"
- **Core Features**:
- **AI as Code**: Configuration-driven AI capability management, supporting version control and team collaboration
- **Workspace Driver**: Project-centered AI environment isolation and management
- **MCP Ecological Deep Integration**: Full support for MCP protocol, rich built-in tools and dynamic loading
- **Multi-platform unification**: Web application, Electron desktop, CLI command line, VSCode plug-in
- **Technical Highlights**:
- Configurable AI agent system, supporting professional Agent customization
- Multi-model parallel comparison testing (Claude, OpenAI, Gemini, etc.)
- Intelligent content rendering (Artifacts, Mermaid, mathematical formulas)
- Scheduled tasks and workflow automation