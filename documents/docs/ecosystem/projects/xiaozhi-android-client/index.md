---
title: Small smartphone terminal
description: Cross-platform Xiaozhi client based on Flutter, supporting multiple platforms such as iOS, Android, and Web
---

#小 Smartphone client

<div class="project-header">
  <div class="project-logo">
<img src="https://avatars.githubusercontent.com/u/196275872?s=48&v=4" alt="Xiaozhi mobile client">
  </div>
  <div class="project-badges">
<span class="badge platform">Multi-platform</span>
    <span class="badge language">Flutter/Dart</span>
<span class="badge status">Active development</span>
  </div>
</div>

## Project Introduction

The Xiaozhi mobile client is a cross-platform application developed based on the Flutter framework, providing mobile access capabilities to the Xiaozhi AI ecosystem. Through a set of codes, it has been deployed on multiple platforms such as iOS, Android, Web, Windows, macOS and Linux, allowing users to conduct real-time voice interaction and text conversations with Xiaozhi AI anytime and anywhere.

<div class="app-showcase">
  <div class="showcase-image">
<img src="./images/Interface1.jpg" alt="Application Display" onerror="this.src='./images/Interface1.jpg'; this.onerror=null;">
    <div class="overlay">
<a href="https://www.bilibili.com/video/BV1fgXvYqE61" target="_blank" class="watch-demo">Watch the demo video</a>
    </div>
  </div>
  <div class="showcase-description">
<p>The latest version of the client has been fully upgraded, supports iOS and Android platforms, and can be self-packaged into Web and PC versions. Through a carefully designed UI and smooth interactive experience, users are provided with the ability to communicate with Xiaozhi AI anytime and anywhere. </p>
  </div>
</div>

## Core functions

<div class="features-grid">
  <div class="feature-card">
    <div class="feature-icon">📱</div>
<h3>Cross-platform support</h3>
<p>Developed using Flutter, one set of code supports multiple platforms such as iOS, Android, Web, Windows, macOS and Linux</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🤖</div>
<h3>Multiple AI model integration</h3>
<p>Supports Xiaozhi AI service, Dify, OpenAI and other AI services, and can switch between different models at any time</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">💬</div>
<h3>Rich interaction methods</h3>
<p>Supports real-time voice conversations, text messages, picture messages, and manual interruption during calls</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🔊</div>
<h3>Voice optimization technology</h3>
<p>Realize AEC+NS echo cancellation for Android devices and improve the quality of voice interaction</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">🎨</div>
<h3>Exquisite interface design</h3>
<p>Lightly skeuomorphic design, smooth animation effects, adaptive UI layout</p>
  </div>
  
  <div class="feature-card">
    <div class="feature-icon">⚙️</div>
<h3>Flexible configuration options</h3>
<p>Supports multiple AI service configuration management, and can add multiple Xiaozhi to the chat list</p>
  </div>
</div>

## Feature Highlights

### Real-time voice interaction

<div class="feature-highlight">
  <div class="highlight-image">
<img src="./images/Interface1.jpg" alt="Real-time voice interaction" onerror="this.src='./images/Interface1.jpg'; this.onerror=null;">
  </div>
  <div class="highlight-content">
<h3>Smooth voice conversation experience</h3>
    <ul>
<li>Real-time speech recognition and response</li>
<li>Support continuous conversation mode</li>
<li>Supports manual interruption during voice interaction</li>
<li>Press and hold to speak shortcut mode</li>
<li>Voice conversation history</li>
    </ul>
  </div>
</div>

### Multiple AI service support

<div class="feature-highlight reverse">
  <div class="highlight-content">
<h3>Flexibly switch between different AI services</h3>
    <ul>
<li>Integrated Xiaozhi WebSocket real-time voice conversation</li>
<li>Support Dify platform access</li>
<li>Support OpenAI graphic messages and streaming output</li>
<li>Supports one-click device registration with official Xiaozhi service</li>
<li>Can add multiple AI services to the conversation list at the same time</li>
    </ul>
  </div>
  <div class="highlight-image">
<img src="./images/Interface 2.jpg" alt="Multiple AI service support" onerror="this.src='./images/Interface 2.jpg'; this.onerror=null;">
  </div>
</div>

## System requirements

- **Flutter**: ^3.7.0
- **Dart**: ^3.7.0
- **iOS**: 12.0+
- **Android**: API 21+ (Android 5.0+)
- **Web**: modern browser

## Installation and use

### Installation method

1. Clone the project repository:
```bash
git clone https://github.com/TOM88812/xiaozhi-android-client.git
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the application:
```bash
flutter run
```

### Build release version

```bash
#Androidapp
flutter build apk --release

#iOSapp
flutter build ios --release

#WebApplication
flutter build web --release
```

> **Note**: After iOS compilation is completed, you need to turn on network permissions in Settings-APP

## Configuration instructions

The application supports flexible service configuration management, including:

### Xiaozhi service configuration
- Supports configuring multiple Xiaozhi service addresses
- WebSocket URL settings
- Token authentication
- Custom MAC address

### Dify API configuration
-Supports configuring multiple Dify services
- API key management
- Server URL configuration

### OpenAI configuration
- API key settings
- Model selection
- Parameter adjustment

## Development Plan

<div class="roadmap">
  <div class="roadmap-item done">
    <div class="status-dot"></div>
    <div class="item-content">
<h4>Function implemented</h4>
      <ul>
<li>Supports multiple AI service providers</li>
<li>Support OTA automatic device registration</li>
<li>Enhance speech recognition accuracy</li>
<li>Achieve mixed text and voice conversation</li>
<li>Support OpenAI interface graphic and text interaction</li>
      </ul>
    </div>
  </div>
  
  <div class="roadmap-item progress">
    <div class="status-dot"></div>
    <div class="item-content">
<h4>Under development</h4>
      <ul>
<li>Dark/light theme adaptation</li>
<li>Implementation of echo cancellation on iOS platform</li>
<li>Native ASR speech recognition support</li>
<li>Local wake word function</li>
      </ul>
    </div>
  </div>
  
  <div class="roadmap-item planned">
    <div class="status-dot"></div>
    <div class="item-content">
<h4>Plan implementation</h4>
      <ul>
<li>Support IoT mapping mobile phone operations</li>
<li>Local TTS implementation</li>
<li>Support MCP_Client</li>
<li>OpenAI interface network search function</li>
      </ul>
    </div>
  </div>
</div>

## Project Contribution

Welcome to contribute code to the Xiaozhi mobile client or submit feedback on issues:

- Currently, echo cancellation on iOS has not yet been implemented, and experienced developers are welcome to PR.
- Submit bugs, feature requests or suggestions for improvements
- Share your experience and cases of using Xiaozhi mobile client

## Related links

- [Project GitHub repository](https://github.com/TOM88812/xiaozhi-android-client)
- [Demo video](https://www.bilibili.com/video/BV1fgXvYqE61)
- [Issue Feedback](https://github.com/TOM88812/xiaozhi-android-client/issues)

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

.app-showcase {
  margin: 2rem 0;
  background-color: var(--vp-c-bg-soft);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.showcase-image {
  position: relative;
  width: 100%;
  height: 300px;
}

.showcase-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.showcase-image:hover .overlay {
  opacity: 1;
}

.watch-demo {
  padding: 0.75rem 1.5rem;
  /*background-color: var(--vp-c-brand);*/
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.1s ease;
}

.watch-demo:hover {
  background-color: var(--vp-c-brand-dark);
}

.showcase-description {
  padding: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.6;
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

.feature-highlight {
  display: flex;
  margin: 3rem 0;
  background-color: var(--vp-c-bg-soft);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
}

.feature-highlight.reverse {
  flex-direction: row-reverse;
}

.highlight-image {
  flex: 1;
  min-width: 40%;
}

.highlight-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.highlight-content {
  flex: 1;
  padding: 2rem;
}

.highlight-content h3 {
  color: var(--vp-c-brand);
  margin-top: 0;
  margin-bottom: 1rem;
}

.highlight-content ul {
  padding-left: 1.5rem;
}

.highlight-content li {
  margin-bottom: 0.5rem;
}

.roadmap {
  position: relative;
  margin: 3rem 0;
  padding-left: 2rem;
}

.roadmap:before {
  content: "";
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--vp-c-divider);
}

.roadmap-item {
  position: relative;
  margin-bottom: 2rem;
}

.status-dot {
  position: absolute;
  left: -2rem;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  z-index: 1;
}

.roadmap-item.done .status-dot {
  background-color: rgb(16, 185, 129);
}

.roadmap-item.progress .status-dot {
  background-color: rgb(245, 158, 11);
}

.roadmap-item.planned .status-dot {
  background-color: rgb(99, 102, 241);
}

.item-content {
  background-color: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
}

.item-content h4 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.roadmap-item.done h4 {
  color: rgb(16, 185, 129);
}

.roadmap-item.progress h4 {
  color: rgb(245, 158, 11);
}

.roadmap-item.planned h4 {
  color: rgb(99, 102, 241);
}

@media (max-width: 768px) {
  .feature-highlight, 
  .feature-highlight.reverse {
    flex-direction: column;
  }
  
  .highlight-image {
    height: 200px;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-logo {
    margin-bottom: 1rem;
  }
}
</style> 