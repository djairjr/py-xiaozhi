---
title: Py-Xiaozhi project structure
description: Xiaozhi voice client implemented based on Python, adopts modular design, supports multiple communication protocols and device integration
sidebar: false,
pageClass: architecture-page-class
---
<script setup>
import CoreArchitecture from './components/CoreArchitecture.vue'
import ModuleDetails from './components/ModuleDetails.vue'
import TechnologyStack from './components/TechnologyStack.vue'
import ArchitectureFeatures from './components/ArchitectureFeatures.vue'
</script>

<div class="architecture-page">

# Py-Xiaozhi project structure

<p class="page-description">Xiaozhi voice client implemented based on Python, adopts modular design and supports multiple communication protocols and device integration</p>

## Core architecture
<CoreArchitecture/>

## Module details
<ModuleDetails/>

## Technology stack
<TechnologyStack/>

## Architectural features
<ArchitectureFeatures/>
</div>

<style>
.page-description {
  font-size: 1.125rem;
  color: var(--vp-c-text-2);
  margin-bottom: 2rem;
  line-height: 1.6;
}
</style>

<style>
.architecture-page {
  max-width: 100%;
  padding: 0 2rem;
}
</style>