---
title: xiaozhi-esp32-server
description: Xiaozhi open source server based on ESP32, lightweight and efficient voice interaction service
---

# xiaozhi-esp32-server

<div class="project-header">
  <div class="project-logo">
    <img src="./images/logo.png" alt="xiaozhi-esp32-server Logo" onerror="this.src='/py-xiaozhi/images/logo.png'; this.onerror=null;">
  </div>
  <div class="project-badges">
    <span class="badge platform">ESP32</span>
    <span class="badge language">Python</span>
<span class="badge status">Active development</span>
  </div>
</div>

<div class="project-intro">
<p>xiaozhi-esp32-server is a back-end service provided for the open source smart hardware project <a href="https://github.com/78/xiaozhi-esp32" target="_blank">xiaozhi-esp32</a>, according to <a href="https://ccnphfhqs21z.feishu.cn/wiki/M0XiwldO9iJwHikpXD5cEx71nKh" target="_blank">Xiaozhi Communication Protocol</a> is implemented in Python to help you quickly build a Xiaozhi server. </p>
</div>

## Applicable people

This project needs to be used with ESP32 hardware equipment. If you have purchased ESP32 related hardware, successfully connected the backend service deployed by Brother Xiazhi, and want to independently build your own `xiaozhi-esp32` backend service, then this project is very suitable for you.

<div class="warning-box">
<h3>⚠️ IMPORTANT NOTICE</h3>
  <ol>
<li>This project is open source software and does not have any commercial partnership with any third-party API service provider (including but not limited to speech recognition, large model, speech synthesis and other platforms), and does not provide any form of guarantee for its service quality and financial security. Users are advised to give priority to service providers that hold relevant business licenses and read their service agreements and privacy policies carefully. This software does not host any account keys, does not participate in fund flows, and does not bear the risk of loss of recharge funds. </li>
<li>This project has been established for a short period of time and has not passed the network security evaluation. Please do not use it in a production environment. If you deploy and study this project in a public network environment, be sure to enable protection in the configuration file <code>config.yaml</code>. </li>
  </ol>
</div>

## Core Features

<div class="features-container">
  <div class="feature-item">
    <div class="feature-icon">🔄</div>
<h3>Communication protocol</h3>
<p>Based on the <code>xiaozhi-esp32</code> protocol, data interaction is realized through WebSocket</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">💬</div>
<h3>Dialogue interaction</h3>
<p>Supports wake-up dialogue, manual dialogue and real-time interruption, and automatically sleeps when there is no dialogue for a long time</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🧠</div>
<h3>Intent recognition</h3>
<p>Supports the use of LLM intent recognition and function call function calls to reduce hard-coded intent judgment</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🌐</div>
<h3>Multi-language recognition</h3>
<p>Supports Mandarin, Cantonese, English, Japanese, and Korean (FunASR is used by default)</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🤖</div>
<h3>LLM module</h3>
<p>Supports flexible switching of LLM modules. ChatGLMLLM is used by default, and Alibaba Bailian, DeepSeek, Ollama, etc. can also be used</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🔊</div>
<h3>TTS module</h3>
<p>Supports EdgeTTS (default), Volcano Engine Beanbag TTS and other TTS interfaces to meet speech synthesis needs</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">📝</div>
<h3>Memory function</h3>
<p>Supports three modes: ultra-long memory, local summary memory, and no memory to meet the needs of different scenarios</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🏠</div>
<h3>IOT function</h3>
<p>Support management and registration of device IOT functions, and support intelligent IoT control based on conversation context</p>
  </div>
  
  <div class="feature-item">
    <div class="feature-icon">🖥️</div>
<h3>Smart console</h3>
<p>Provides a Web management interface that supports agent management, user management, system configuration and other functions</p>
  </div>
</div>

## Deployment method

This project provides two deployment methods, please choose according to your specific needs:

<div class="deployment-table">
  <table>
    <thead>
      <tr>
<th>Deployment method</th>
<th>Features</th>
<th>Applicable scenarios</th>
      </tr>
    </thead>
    <tbody>
      <tr>
<td><strong>Easiest installation</strong></td>
<td>Intelligent dialogue, IOT function, data stored in configuration file</td>
<td>Low configuration environment, no database required</td>
      </tr>
      <tr>
<td><strong>Full module installation</strong></td>
<td>Intelligent dialogue, IOT, OTA, intelligent console, data is stored in the database</td>
<td>Full functional experience</td>
      </tr>
    </tbody>
  </table>
</div>

For detailed deployment documentation, please refer to:
- [Docker Deployment Document](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/Deployment.md)
- [Source code deployment documentation](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/Deployment_all.md)

## Supported platform list

xiaozhi-esp32-server supports a variety of third-party platforms and components:

### LLM language model

<div class="platform-item">
<h4>Interface call</h4>
<p><strong>Supported platforms:</strong>Alibaba Bailian, Volcano Engine Doubao, Deep Search, Zhipu ChatGLM, Gemini, Ollama, Dify, Fastgpt, Coze</p>
<p><strong>Free platforms:</strong>ChatGLM, Gemini</p>
<p><em>In fact, any LLM that supports openai interface calls can be accessed and used</em></p>
</div>

### TTS speech synthesis

<div class="platform-item">
<h4>Interface call</h4>
<p><strong>Supported platforms:</strong>EdgeTTS, Volcano Engine Doubao TTS, Tencent Cloud, Alibaba Cloud TTS, CosyVoiceSiliconflow, TTS302AI, CozeCnTTS, GizwitsTTS, ACGNTTS, OpenAITTS</p>
<p><strong>Free platforms:</strong>EdgeTTS, CosyVoiceSiliconflow (part)</p>
  
<h4>Local services</h4>
<p><strong>Supported platforms:</strong>FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3, MinimaxTTS</p>
<p><strong>Free platforms:</strong>FishSpeech, GPT_SOVITS_V2, GPT_SOVITS_V3, MinimaxTTS</p>
</div>

### ASR Speech Recognition

<div class="platform-item">
<h4>Interface call</h4>
<p><strong>Supported platform: </strong>DoubaoASR</p>
  
<h4>Local services</h4>
<p><strong>Supported platforms:</strong>FunASR, SherpaASR</p>
<p><strong>Free platforms:</strong>FunASR, SherpaASR</p>
</div>

### More components

- **VAD Voice Activity Detection**: Supports SileroVAD (free for local use)
- **Memory Storage**: Supports mem0ai (1000 times/month quota), mem_local_short (local summary, free)
- **Intent recognition**: Supports intent_llm (identifying intentions through large models), function_call (completes intentions through large model function calls)

## Participate and contribute

xiaozhi-esp32-server is an active open source project. You are welcome to contribute code or submit feedback:

- [GitHub repository](https://github.com/xinnan-tech/xiaozhi-esp32-server)
- [Problem Feedback](https://github.com/xinnan-tech/xiaozhi-esp32-server/issues)
- [Open letter to developers](https://github.com/xinnan-tech/xiaozhi-esp32-server/blob/main/docs/contributor_open_letter.md)

<style>
.project-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
}

.project-logo {
  width: 100px;
  height: 100px;
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
  background-color: rgba(16, 185, 129, 0.2);
  color: rgb(16, 185, 129);
}

.project-intro {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  border-left: 4px solid var(--vp-c-brand);
}

.warning-box {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: rgba(234, 179, 8, 0.1);
  border-left: 4px solid rgba(234, 179, 8, 0.8);
  border-radius: 8px;
}

.warning-box h3 {
  color: rgb(234, 179, 8);
  margin-top: 0;
}

.features-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-item {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--vp-c-divider);
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.feature-item h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.deployment-table {
  margin: 2rem 0;
  overflow-x: auto;
}

.deployment-table table {
  width: 100%;
  border-collapse: collapse;
}

.deployment-table th, 
.deployment-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--vp-c-divider);
}

.deployment-table th {
  background-color: var(--vp-c-bg-soft);
  font-weight: 500;
}

.platform-item {
  margin: 1.5rem 0;
  padding: 1.5rem;
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
}

.platform-item h4 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 1rem;
}

.platform-item p {
  margin: 0.5rem 0;
}

.demo-videos {
  margin: 2rem 0;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.video-item {
  display: block;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
  background-color: var(--vp-c-bg-soft);
}

.video-item:hover {
  transform: translateY(-5px);
}

.video-thumbnail {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.video-item:hover .video-thumbnail img {
  transform: scale(1.05);
}

.video-title {
  padding: 1rem;
  font-weight: 500;
}

.demo-more {
  text-align: center;
  margin-top: 1.5rem;
}

.demo-more a {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  background-color: var(--vp-c-brand);
  color: white;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.demo-more a:hover {
  background-color: var(--vp-c-brand-dark);
}

.related-projects {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.project-card {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--vp-c-divider);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.project-card h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 1rem;
}

.project-link {
  margin-top: auto;
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: var(--vp-c-brand);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
  transition: background-color 0.3s ease;
}

.project-link:hover {
  background-color: var(--vp-c-brand-dark);
}

.contributors {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.contributor {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  border: 1px solid var(--vp-c-divider);
}

.contributor img {
  width: 120px;
  height: 60px;
  object-fit: contain;
  margin-bottom: 1rem;
}

.contributor h4 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
  
  .contributors {
    grid-template-columns: 1fr;
  }
  
  .related-projects {
    grid-template-columns: 1fr;
  }
  
  .features-container {
    grid-template-columns: 1fr;
  }
}
</style> 