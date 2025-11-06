---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "PY-XIAOZHI"
tagline: py-xiaozhi is a Xiaozhi voice client implemented in Python, designed to learn through code and experience the AI ​​Xiaozhi voice function without hardware conditions.
  actions:
    - theme: brand
text: Get started
link: /guide/documentation directory
    - theme: alt
text: View source code
      link: https://github.com/huangjunsen0406/py-xiaozhi

features:
- title: AI voice interaction
details: Supports voice input and recognition, realizes intelligent human-computer interaction, and provides a natural and smooth conversation experience. Designed with an asynchronous architecture, it supports real-time audio processing and low-latency response.
- title: Visual multimodality
details: Support image recognition and processing, provide multi-modal interaction capabilities, and understand image content. Integrated OpenCV camera processing to support real-time visual analysis.
- title: MCP Tool Server
details: A modular tool system based on JSON-RPC 2.0 protocol, supporting rich functions such as schedule management, music playback, 12306 query, map service, recipe search, numerology, etc., and can dynamically expand tool plug-ins.
- title: IoT device integration
details: Designed using Thing abstract mode, it supports smart home device control, including lights, volume, temperature sensors, etc., and integrates the Home Assistant smart home platform, which can be easily expanded.
- title: High performance audio processing
Details: Real-time audio transmission based on Opus codec, supports intelligent resampling technology, and 5ms audio frame interval processing to ensure a low-latency and high-quality audio experience.
- title: Cross-platform support
details: Compatible with Windows 10+, macOS 10.15+ and Linux systems, supports GUI and CLI dual-mode operation, and adapts to audio devices and system interfaces on different platforms.
---

<style>
.developers-section {
  text-align: center;
  max-width: 960px;
  margin: 4rem auto 0;
  padding: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.developers-section h2 {
  margin-bottom: 0.5rem;
  color: var(--vp-c-brand);
}

.contributors-wrapper {
  margin: 2rem auto;
  max-width: 800px;
  position: relative;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.contributors-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.contributors-link {
  display: block;
  text-decoration: none;
  background-color: var(--vp-c-bg-soft);
}

.contributors-image {
  width: 100%;
  height: auto;
  display: block;
  transition: all 0.3s ease;
}

.developers-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.developers-actions a {
  text-decoration: none;
}

.dev-button {
  display: inline-block;
  border-radius: 20px;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-decoration: none;
}

.dev-button:not(.outline) {
  background-color: var(--vp-c-brand);
  color: white;
}

.dev-button.outline {
  border: 1px solid var(--vp-c-brand);
  color: var(--vp-c-brand);
}

.dev-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 640px) {
  .developers-actions {
    flex-direction: column;
  }
  
  .contributors-wrapper {
    margin: 1.5rem auto;
  }
}

.join-message {
  text-align: center;
  margin-top: 2rem;
  padding: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.join-message h3 {
  margin-bottom: 1rem;
}
</style>
