---
title: open-xiaoai
description: Let Xiaoai Speaker "hear your voice" and unlock unlimited possibilities for open source projects
---

# open-xiaoai

<div class="project-header">
  <div class="project-logo">
    <img src="https://avatars.githubusercontent.com/u/35302658?s=48&v=4" alt="open-xiaoai Logo">
  </div>
  <div class="project-badges">
<span class="badge platform">Cross-platform</span>
    <span class="badge language">Rust/Python/Node.js</span>
<span class="badge status">Experimental</span>
  </div>
</div>

<div class="project-banner">
<img src="./images/logo.png" alt="Open-XiaoAI project cover">
</div>

## Project Introduction

Open-XiaoAI is an open source project that allows Xiaoai speakers to "hear your voice" and seamlessly integrates Xiaoai speakers with the Xiaozhi AI ecosystem. This project directly takes over the "ears" and "mouth" of Xiaoai speakers, and uses multi-modal large models and AI Agent technology to fully unleash the potential of Xiaoai speakers and unlock unlimited possibilities.

In 2017, when the world's first smart speaker with a sales volume of tens of millions was born, we thought we had touched the future. But it was quickly discovered that these devices were trapped in a "command-response" cage:

- It can hear decibels, but it cannot understand emotions
- It can execute commands but does not think actively
- It has millions of users, but only one set of thinking

The "Jarvis" level artificial intelligence we once imagined has been reduced to an "alarm clock + music player" in real scenarios.

**True intelligence should not be bound by preset code logic, but should evolve through interaction like a living organism. **

Based on the previous [MiGPT](https://github.com/idootop/mi-gpt) project, Open-XiaoAI has evolved again, providing the Xiaozhi ecosystem with a new way to interact with Xiaoai speakers.

## Core functions

<div class="features-grid">
  <div class="feature-card">
    <div class="feature-icon">🎤</div>
<h3>Voice input takeover</h3>
<p>Directly capture the microphone input of Xiaoai speakers, bypassing the original speech recognition limitations</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔊</div>
<h3>Sound output control</h3>
<p>Completely takes over the speaker of Xiaoai Speaker and can play customized audio and TTS content</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🧠</div>
<h3>AI model integration</h3>
<p>Supports access to multiple large models such as Xiaozhi AI and ChatGPT to achieve a natural conversation experience</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🌐</div>
<h3>Cross-platform support</h3>
<p>The client is developed using Rust, and the server supports Python and Node.js</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🛠️</div>
<h3>Scalable architecture</h3>
<p>Modular design makes it easy for developers to add custom functions and integrate other services</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🎮</div>
<h3>Developer friendly</h3>
<p>Detailed documentation and tutorials help developers quickly get started and customize their own functions</p>
  </div>
</div>

## Demo video

<div class="demo-videos">
  <div class="video-item">
    <a href="https://www.bilibili.com/video/BV1NBXWYSEvX" target="_blank" class="video-link">
      <div class="video-thumbnail">
<img src="https://raw.githubusercontent.com/idootop/open-xiaoai/main/docs/images/xiaozhi.jpg" alt="Xiaozhi Speaker is connected to Xiaozhi AI">
      </div>
      <div class="video-title">
        <span class="video-icon">▶️</span>
<span>Demonstration of connecting Xiaoai speakers to Xiaozhi AI</span>
      </div>
    </a>
  </div>
  
  <div class="video-item">
    <a href="https://www.bilibili.com/video/BV1N1421y7qn" target="_blank" class="video-link">
      <div class="video-thumbnail">
<img src="https://github.com/idootop/open-xiaoai/raw/main/docs/images/migpt.jpg" alt="Xiaoai speakers are connected to MiGPT">
      </div>
      <div class="video-title">
        <span class="video-icon">▶️</span>
<span>Demonstration of connecting Xiaoai speakers to MiGPT</span>
      </div>
    </a>
  </div>
</div>

## Quick start

<div class="important-notice">
  <div class="notice-icon">⚠️</div>
  <div class="notice-content">
<strong>Important Tip</strong>
<p>This tutorial is only applicable to <strong>Xiaomi Smart Speaker Pro (LX06)</strong> and <strong>Xiaomi Smart Speaker Pro (OH2P)</strong>. Please do not use <strong>Other models</strong> of Xiaoai speakers directly! </p>
  </div>
</div>

The Open-XiaoAI project consists of two parts: Client and Server. You can start quickly by following the steps below:

### Installation steps

<div class="steps">
  <div class="step">
    <div class="step-number">1</div>
    <div class="step-content">
<h4>Xiaoai speaker firmware update</h4>
<p>Update the Xiaoai Speaker patch firmware by flashing it, open it and connect to Xiaoai Speaker via SSH</p>
<a href="https://github.com/idootop/open-xiaoai/blob/main/docs/flash.md" target="_blank" class="step-link">View detailed tutorial</a>
    </div>
  </div>
  
  <div class="step">
    <div class="step-number">2</div>
    <div class="step-content">
<h4>Client deployment</h4>
<p>Compile the client patch program on your computer, then copy it to the Xiaoai speaker and run it</p>
<a href="https://github.com/idootop/open-xiaoai/blob/main/packages/client-rust/README.md" target="_blank" class="step-link">View detailed tutorial</a>
    </div>
  </div>
  
  <div class="step">
    <div class="step-number">3</div>
    <div class="step-content">
<h4>Server-side deployment</h4>
<p>Run the server-side demo program on your computer to experience the new capabilities of Xiaoai speakers</p>
      <ul class="step-options">
<li><a href="https://github.com/idootop/open-xiaoai/blob/main/packages/server-python/README.md" target="_blank">Python Server - Xiaoai Speaker is connected to Xiaozhi AI</a></li>
<li><a href="https://github.com/idootop/open-xiaoai/blob/main/packages/server-node/README.md" target="_blank">Node.js Server - Xiaoai Speaker connected to MiGPT-Next</a></li>
      </ul>
    </div>
  </div>
</div>

## Working principle

Open-XiaoAI works in the following ways:

1. **Firmware patch**: Modify the firmware of Xiaoai speakers to allow SSH access and underlying system control
2. **Audio Stream Hijacking**: Client program directly captures microphone input and controls speaker output
3. **Network Communication**: Establish a WebSocket connection between the client and the server for real-time communication
4. **AI processing**: The server receives the voice input, processes it by the AI ​​model and returns a response.
5. **Custom functions**: Developers can implement various custom functions and integrations on the server side

## Related projects

If you don’t want to flash your phone, or it’s not Xiaoai Speaker Pro, the following items may be useful to you:

- [MiGPT](https://github.com/idootop/mi-gpt) - The original project of connecting ChatGPT to Xiaoai Speaker
- [MiGPT-Next](https://github.com/idootop/migpt-next) - The next generation version of MiGPT
- [XiaoGPT](https://github.com/yihong0618/xiaogpt) - Another Xiaoai speaker ChatGPT access solution
- [XiaoMusic](https://github.com/hanxi/xiaomusic) - Xiaoai speaker music playback enhancement

## Technical Reference

If you want more technical details, the following links may be helpful:

- [xiaoai-patch](https://github.com/duhow/xiaoai-patch) - Xiaoai speaker firmware patch
- [open-lx01](https://github.com/jialeicui/open-lx01) - Xiaoai Speaker LX01 open source project
- [Xiaoai FM Research](https://javabin.cn/2021/xiaoai_fm.html) - Xiaoai Speaker FM Function Research
- [Xiaomi device security research](https://github.com/yihong0618/gitblog/issues/258) - Xiaomi IoT device security analysis
- [Exploration of Xiaoai Speaker](https://xuanxuanblingbling.github.io/iot/2022/09/16/mi/) - Exploration of Xiaoai Speaker Technology

## Disclaimer

<div class="disclaimer">
<h4>Scope of application</h4>
<p>This project is a non-profit open source project, limited to technical principle research, security vulnerability verification and non-profit personal use. It is strictly prohibited to use it in scenarios such as commercial services, network attacks, data theft, system damage, etc. that violate the Cybersecurity Law and the legal provisions of the jurisdiction where the user is located. </p>
  
<h4>Unofficial statement</h4>
<p>This project was independently developed by a third-party developer and has no affiliation/cooperation relationship with Xiaomi Group and its affiliates (hereinafter referred to as "rights parties"), and has not received official authorization/recognition or technical support from them. All rights to the trademarks, firmware, and cloud services involved in the project belong to Xiaomi Group. If the right party claims rights, the user should immediately stop using and delete this item. </p>
  
<p>Continuing to use this project means that you have fully read and agreed to the <a href="https://github.com/idootop/open-xiaoai/blob/main/agreement.md" target="_blank">User Agreement</a>. Otherwise, please terminate use immediately and completely delete this project. </p>
</div>

## License

This project uses the [MIT](https://github.com/idootop/open-xiaoai/blob/main/LICENSE) license © 2024-PRESENT Del Wang

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
  background-color: rgba(139, 92, 246, 0.2);
  color: rgb(139, 92, 246);
}

.project-banner {
  width: 100%;
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.project-banner img {
  width: 100%;
  height: auto;
  display: block;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-card {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid var(--vp-c-divider);
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.demo-videos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.video-item {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.video-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.video-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.video-thumbnail {
  width: 100%;
  height: 180px;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.video-icon {
  color: var(--vp-c-brand);
}

.important-notice {
  background-color: rgba(234, 179, 8, 0.1);
  border-left: 4px solid rgba(234, 179, 8, 0.8);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.5rem;
  margin: 2rem 0;
  display: flex;
  gap: 1rem;
}

.notice-icon {
  font-size: 1.5rem;
}

.notice-content strong {
  display: block;
  margin-bottom: 0.5rem;
}

.steps {
  margin: 2rem 0;
}

.step {
  display: flex;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: var(--vp-c-brand);
  color: white;
  border-radius: 50%;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--vp-c-brand);
}

.step-link {
  display: inline-block;
  margin-top: 0.5rem;
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
}

.step-link:hover {
  text-decoration: underline;
}

.step-options {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-top: 0.5rem;
}

.architecture-diagram {
  text-align: center;
  margin: 2rem 0;
}

.architecture-diagram img {
  max-width: 100%;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

.disclaimer {
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 4px solid rgba(239, 68, 68, 0.8);
  border-radius: 0 8px 8px 0;
  padding: 1.5rem;
  margin: 2rem 0;
}

.disclaimer h4 {
  margin-top: 0;
  color: rgba(239, 68, 68, 0.8);
  margin-bottom: 0.5rem;
}

.disclaimer p {
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
  
  .demo-videos {
    grid-template-columns: 1fr;
  }
}
</style> 