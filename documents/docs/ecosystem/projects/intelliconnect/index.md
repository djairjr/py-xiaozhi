---
title: IntelliConnect
description: An intelligent IoT platform based on SpringBoot, an IoT solution integrating Agent intelligence technology
---

# IntelliConnect

<div class="project-header">
  <div class="project-logo">
    <img src="./images/logo.png" alt="IntelliConnect Logo">
  </div>
  <div class="project-badges">
<span class="badge platform">Cross-platform</span>
    <span class="badge language">Java/Spring</span>
    <span class="badge status">v0.1</span>
  </div>
</div>

<div class="ascii-art">
<pre>
██╗ ███╗   ██╗ ████████╗ ███████╗ ██╗      ██╗      ██╗    ██████╗  ██████╗  ███╗   ██╗ ███╗   ██╗ ███████╗  ██████╗ ████████╗
██║ ████╗  ██║ ╚══██╔══╝ ██╔════╝ ██║      ██║      ██║   ██╔════╝ ██╔═══██╗ ████╗  ██║ ████╗  ██║ ██╔════╝ ██╔════╝ ╚══██╔══╝
██║ ██╔██╗ ██║    ██║    █████╗   ██║      ██║      ██║   ██║      ██║   ██║ ██╔██╗ ██║ ██╔██╗ ██║ █████╗   ██║         ██║   
██║ ██║╚██╗██║    ██║    ██╔══╝   ██║      ██║      ██║   ██║      ██║   ██║ ██║╚██╗██║ ██║╚██╗██║ ██╔══╝   ██║         ██║   
██║ ██║ ╚████║    ██║    ███████╗ ███████╗ ███████╗ ██║   ╚██████╗ ╚██████╔╝ ██║ ╚████║ ██║ ╚████║ ███████╗ ╚██████╗    ██║   
╚═╝ ╚═╝  ╚═══╝    ╚═╝    ╚══════╝ ╚══════╝ ╚══════╝ ╚═╝    ╚═════╝  ╚═════╝  ╚═╝  ╚═══╝ ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝    ╚═╝   
</pre>
<p class="ascii-caption">Built by RSLLY</p>
</div>

<div class="project-badges-center">
  <img src="https://img.shields.io/badge/license-apache2.0-yellow?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/release-v0.1-blue?style=flat-square" alt="Release" />
  <img src="https://img.shields.io/badge/cwl-project1.8-green?style=flat-square" alt="CWL Project" />
</div>

## Overview

* This project is developed based on springboot2.7 and uses spring security as the security framework
* Equipped object model (property, function and event module) and complete monitoring module
* Supports a variety of large models and advanced Agent intelligence technology to provide excellent AI intelligence and can quickly build intelligent IoT applications (the first IoT platform based on Agent intelligence design)
* Supports rapid construction of intelligent voice applications, speech recognition and speech synthesis
* Supports multiple IoT protocols, uses emqx exhook as mqtt communication, and has strong scalability
* Support OTA air upgrade technology
* Support WeChat mini program and WeChat service account
* Support Xiaozhi AI hardware
* Use common mysql and redis databases, easy to get started
* Support time series database influxdb

## Install and run

<div class="notice">
<p>It is recommended to use docker for installation. The docker-compose.yaml file is in the docker directory. Execute docker-compose up to initialize the mysql, redis, emqx and influxdb environments. Please see the official documentation for installation details. </p>
</div>

* Install mysql and redis databases. For high-performance operation, it is recommended to install the time series database influxdb.
* Install the EMQX cluster and configure exhook. This project uses exhook as the processor of mqtt messages
* Install java17 environment
* Modify the configuration file application.yaml (set ddl-auto to update mode)
* java -jar IntelliConnect-1.8-SNAPSHOT.jar

```bash
# Clone repository
git clone https://github.com/ruanrongman/IntelliConnect
cd intelliconnect/docker

# Start the required environment (MySQL, Redis, EMQX, InfluxDB)
docker-compose up -d
```

## Project Features

* Minimalism, clear layers, in line with mvc hierarchical structure
* Complete object model abstraction allows IoT developers to focus on the business itself
* Rich AI capabilities, support Agent intelligent technology, rapid development of AI intelligent applications

## Xiaozhi ESP-32 backend service (xiaozhi-esp32-server)

<div class="esp32-section">
<p>This project can provide back-end services for the open source smart hardware project <a href="https://github.com/78/xiaozhi-esp32" target="_blank">xiaozhi-esp32</a>. Implemented using <code>Java</code> according to <a href="https://ccnphfhqs21z.feishu.cn/wiki/M0XiwldO9iJwHikpXD5cEx71nKh" target="_blank">Xiao Zhi Communication Protocol</a>. </p>
<p>Suitable for users who want to deploy locally. Different from pure voice interaction, the focus of this project is to provide more powerful Internet of Things and intelligent agent capabilities. </p>
</div>

## Project documentation and video demonstrations

* Project document and video demonstration address: [https://ruanrongman.github.io/IntelliConnect/](https://ruanrongman.github.io/IntelliConnect/)
*Technical blog address: [https://wordpress.rslly.top](https://wordpress.rslly.top)
* Community address: [https://github.com/cwliot](https://github.com/cwliot)
* Chuangwanlian community public account: Search Chuangwanlian directly on WeChat

## Related projects and communities

* **Chuangwanlian(cwl)**: An open source community focusing on Internet of Things and artificial intelligence technology.
* **Promptulate**: [https://github.com/Undertone0809/promptulate](https://github.com/Undertone0809/promptulate) - A LLM application and Agent development framework.
* **Rymcu**: [https://github.com/rymcu](https://github.com/rymcu) - an open source embedded knowledge learning and exchange platform serving millions of people

## Acknowledgments

* 感谢项目[xiaozhi-esp32](https://github.com/78/xiaozhi-esp32)提供强大的硬件语音交互。
* Thanks to the project [Concentus: Opus for Everyone](https://github.com/lostromb/concentus) for providing opus decoding and encoding.
* Thanks to the project [TalkX](https://github.com/big-mouth-cn/talkx) for providing the reference for opus decoding and encoding.
* Thanks to the project [py-xiaozhi](https://github.com/huangjunsen0406/py-xiaozhi) for facilitating the development and debugging of the project.

## contribute

I am trying some more complete abstract modes to support more IoT protocols and data storage forms. If you have better suggestions, please feel free to discuss and exchange them.

<style>
.project-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.project-logo {
  width: 120px;
  height: 120px;
  margin-right: 1.5rem;
}

.project-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.project-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.platform {
  background-color: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-dark);
}

.badge.language {
  background-color: rgba(59, 130, 246, 0.2);
  color: rgb(59, 130, 246);
}

.badge.status {
  background-color: rgba(234, 179, 8, 0.2);
  color: rgb(234, 179, 8);
}

.ascii-art {
  overflow-x: auto;
  margin: 2rem 0;
  text-align: center;
}

.ascii-art pre {
  display: inline-block;
  text-align: left;
  font-size: 0.6rem;
  line-height: 1;
  white-space: pre;
  margin: 0;
  background: transparent;
  color: var(--vp-c-brand);
  font-family: monospace;
}

.ascii-caption {
  font-size: 0.8rem;
  margin-top: 0.5rem;
  color: var(--vp-c-text-2);
}

.project-badges-center {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.notice {
  background-color: var(--vp-c-bg-soft);
  border-left: 4px solid var(--vp-c-brand);
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 8px 8px 0;
}

.esp32-section {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border: 1px solid var(--vp-c-divider);
}

.qr-container {
  text-align: center;
  margin: 2rem 0;
}

.qr-code {
  width: 250px;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

@media (max-width: 768px) {
  .ascii-art pre {
    font-size: 0.4rem;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  .ascii-art {
    display: none;
  }
}
</style> 