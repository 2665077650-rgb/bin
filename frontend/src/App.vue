<template>
  <div id="app" :class="{'dark-mode': isDarkMode}">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-left">
        <router-link to="/" class="logo">
          <div class="logo-icon">
            <span class="logo-char">时</span>
            <span class="logo-char">空</span>
          </div>
          <h1>时空博物馆</h1>
        </router-link>
      </div>

      <nav class="header-nav">
        <router-link to="/" class="nav-link">
          <FontAwesomeIcon icon="home" />
          <span>首页</span>
        </router-link>
        <router-link to="/virtual-tour" class="nav-link">
          <FontAwesomeIcon icon="compass" />
          <span>虚拟展厅</span>
        </router-link>
        <router-link to="/time-map" class="nav-link">
          <FontAwesomeIcon icon="map" />
          <span>时空地图</span>
        </router-link>
        <router-link to="/repair-lab" class="nav-link">
          <FontAwesomeIcon icon="puzzle-piece" />
          <span>修复实验室</span>
        </router-link>
      </nav>

      <div class="header-right">
        <button class="icon-btn" @click="toggleDarkMode">
          <FontAwesomeIcon :icon="isDarkMode ? 'lightbulb' : 'palette'" />
        </button>
        <button class="icon-btn">
          <FontAwesomeIcon icon="search" />
        </button>
        <button class="icon-btn">
          <FontAwesomeIcon icon="user" />
        </button>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部播放栏（音乐/解说） -->
    <footer class="audio-player" v-if="currentAudio">
      <div class="audio-info">
        <div class="audio-thumbnail"></div>
        <div class="audio-details">
          <h4>{{ currentAudio.title }}</h4>
          <p>{{ currentAudio.artist }}</p>
        </div>
      </div>
      <div class="audio-controls">
        <button class="control-btn">
          <FontAwesomeIcon icon="times" />
        </button>
        <button class="control-btn">
          <FontAwesomeIcon icon="arrow-left" />
        </button>
        <button class="control-btn play-btn" @click="togglePlay">
          <FontAwesomeIcon :icon="isPlaying ? 'volume-up' : 'volume-up'" />
        </button>
        <button class="control-btn">
          <FontAwesomeIcon icon="arrow-right" />
        </button>
        <button class="control-btn">
          <FontAwesomeIcon icon="expand" />
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isDarkMode = ref(false)
const isPlaying = ref(false)
const currentAudio = ref(null)

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light')
}

const togglePlay = () => {
  isPlaying.value = !isPlaying.value
}

// 监听路由变化
router.afterEach(() => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--header-bg);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
  border-bottom: 1px solid var(--border-color);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--text-primary);
}

.logo-icon {
  display: flex;
  gap: 2px;
}

.logo-char {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  border-radius: 6px;
}

.logo h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.header-nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 12px;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
}

.nav-link svg {
  font-size: 20px;
}

.header-right {
  display: flex;
  gap: 16px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--surface);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.icon-btn:hover {
  background: var(--surface-hover);
  transform: translateY(-2px);
}

.app-main {
  margin-top: 64px;
  min-height: calc(100vh - 64px - 80px);
}

.audio-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 80px;
  background: var(--surface);
  border-top: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
}

.audio-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.audio-thumbnail {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 8px;
}

.audio-details h4 {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: var(--text-primary);
}

.audio-details p {
  margin: 0;
  font-size: 12px;
  color: var(--text-secondary);
}

.audio-controls {
  display: flex;
  gap: 16px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: var(--surface);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.control-btn:hover {
  background: var(--surface-hover);
}

.play-btn {
  background: var(--primary);
  color: white;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:root {
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --surface: #ffffff;
  --surface-hover: #f3f4f6;
  --border-color: #e5e7eb;
  --header-bg: rgba(255, 255, 255, 0.8);
}

[data-theme="dark"] {
  --primary: #8b5cf6;
  --secondary: #ec4899;
  --text-primary: #f9fafb;
  --text-secondary: #d1d5db;
  --bg-primary: #111827;
  --bg-secondary: #1f2937;
  --surface: #1f2937;
  --surface-hover: #374151;
  --border-color: #374151;
  --header-bg: rgba(31, 41, 55, 0.8);
}

#app.dark-mode {
  background: var(--bg-primary);
  color: var(--text-primary);
}
</style>