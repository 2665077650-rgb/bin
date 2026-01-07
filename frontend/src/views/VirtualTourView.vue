<template>
  <div class="virtual-tour-view">
    <!-- 3D展厅主区域 -->
    <div class="tour-container">
      <!-- 左侧导航 -->
      <aside class="tour-sidebar">
        <div class="sidebar-header">
          <h3><FontAwesomeIcon icon="compass" /> 虚拟展厅</h3>
          <p>漫步千年历史，触摸文明脉搏</p>
        </div>

        <div class="exhibition-list">
          <div class="exhibition-item active">
            <div class="exhibition-icon">
              <FontAwesomeIcon icon="dragon" />
            </div>
            <div class="exhibition-info">
              <h4>主展厅</h4>
              <p>青铜器专题</p>
              <span class="artifact-count">15件文物</span>
            </div>
          </div>

          <div class="exhibition-item">
            <div class="exhibition-icon">
              <FontAwesomeIcon icon="gem" />
            </div>
            <div class="exhibition-info">
              <h4>玉石馆</h4>
              <p>古代玉器珍藏</p>
              <span class="artifact-count">28件文物</span>
            </div>
          </div>

          <div class="exhibition-item">
            <div class="exhibition-icon">
              <FontAwesomeIcon icon="vase" />
            </div>
            <div class="exhibition-info">
              <h4>陶瓷馆</h4>
              <p>唐宋瓷器艺术</p>
              <span class="artifact-count">42件文物</span>
            </div>
          </div>
        </div>

        <div class="current-location">
          <h4>当前位置</h4>
          <div class="location-info">
            <FontAwesomeIcon icon="map-marker-alt" />
            <span>主展厅 - 青铜器区</span>
          </div>
          <div class="online-status">
            <div class="status-dot online"></div>
            <span>在线人数：2,348</span>
          </div>
        </div>
      </aside>

      <!-- 3D视图区域 -->
      <main class="tour-main">
        <div class="viewer-header">
          <div class="viewer-controls">
            <button class="control-btn" :class="{active: activeControl === 'move'}"
                    @click="setControl('move')">
              <FontAwesomeIcon icon="arrows" />
              <span>移动</span>
            </button>
            <button class="control-btn" :class="{active: activeControl === 'rotate'}"
                    @click="setControl('rotate')">
              <FontAwesomeIcon icon="rotate" />
              <span>旋转</span>
            </button>
            <button class="control-btn" :class="{active: activeControl === 'zoom'}"
                    @click="setControl('zoom')">
              <FontAwesomeIcon icon="search" />
              <span>缩放</span>
            </button>
            <button class="control-btn">
              <FontAwesomeIcon icon="expand" />
              <span>全屏</span>
            </button>
          </div>

          <div class="viewer-stats">
            <div class="stat-item">
              <FontAwesomeIcon icon="eye" />
              <span>{{ viewCount }}</span>
            </div>
            <div class="stat-item">
              <FontAwesomeIcon icon="clock" />
              <span>{{ formatTime(elapsedTime) }}</span>
            </div>
          </div>
        </div>

        <!-- 3D场景容器 -->
        <div class="scene-container" ref="sceneContainer">
          <div class="scene-placeholder">
            <div class="artifact-markers">
              <div v-for="marker in markers" :key="marker.id"
                   class="artifact-marker"
                   :style="{left: marker.x + '%', top: marker.y + '%'}"
                   @click="selectArtifact(marker)">
                <div class="marker-dot"></div>
                <div class="marker-label">{{ marker.name }}</div>
              </div>
            </div>

            <div class="scene-info">
              <h4>3D虚拟展厅</h4>
              <p>拖拽旋转视角 • 滚轮缩放 • WASD移动</p>
              <div class="loading-progress" v-if="loading">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{width: loadingProgress + '%'}"></div>
                </div>
                <span>加载中... {{ loadingProgress }}%</span>
              </div>
              <button v-else class="btn btn-primary" @click="enterVR">
                <FontAwesomeIcon icon="vr-cardboard" />
                <span>进入VR模式</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 文物详情面板 -->
        <div class="artifact-panel" :class="{active: selectedArtifact}">
          <div class="panel-header">
            <h3>{{ selectedArtifact?.name || '选择文物' }}</h3>
            <button class="close-btn" @click="selectedArtifact = null">
              <FontAwesomeIcon icon="times" />
            </button>
          </div>

          <div v-if="selectedArtifact" class="panel-content">
            <div class="artifact-preview">
              <div class="preview-image" :style="`background-image: url(${selectedArtifact.image})`"></div>
              <div class="preview-controls">
                <button class="preview-btn">
                  <FontAwesomeIcon icon="rotate-left" />
                </button>
                <button class="preview-btn">
                  <FontAwesomeIcon icon="expand" />
                </button>
                <button class="preview-btn" @click="viewDetail(selectedArtifact.id)">
                  <FontAwesomeIcon icon="info-circle" />
                </button>
              </div>
            </div>

            <div class="artifact-info">
              <div class="info-row">
                <label>年代</label>
                <span>{{ selectedArtifact.era }}</span>
              </div>
              <div class="info-row">
                <label>材质</label>
                <span>{{ selectedArtifact.material }}</span>
              </div>
              <div class="info-row">
                <label>出土地</label>
                <span>{{ selectedArtifact.location }}</span>
              </div>
              <div class="info-row">
                <label>尺寸</label>
                <span>{{ selectedArtifact.dimensions }}</span>
              </div>

              <div class="description">
                <h4>文物介绍</h4>
                <p>{{ selectedArtifact.description }}</p>
              </div>

              <div class="artifact-actions">
                <button class="btn btn-primary" @click="startAIGuide(selectedArtifact.id)">
                  <FontAwesomeIcon icon="robot" />
                  <span>AI解说</span>
                </button>
                <button class="btn btn-outline">
                  <FontAwesomeIcon icon="bookmark" />
                  <span>收藏</span>
                </button>
                <button class="btn btn-outline">
                  <FontAwesomeIcon icon="share" />
                  <span>分享</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="panel-empty">
            <FontAwesomeIcon icon="compass" />
            <p>点击展厅中的标记点查看文物详情</p>
          </div>
        </div>
      </main>
    </div>

    <!-- 底部快捷导航 -->
    <div class="quick-nav">
      <button class="nav-btn" @click="showMap = !showMap">
        <FontAwesomeIcon icon="map" />
        <span>展厅地图</span>
      </button>
      <button class="nav-btn" @click="showGuide = !showGuide">
        <FontAwesomeIcon icon="question-circle" />
        <span>参观指南</span>
      </button>
      <button class="nav-btn" @click="toggleAudioGuide">
        <FontAwesomeIcon :icon="audioPlaying ? 'volume-up' : 'volume-mute'" />
        <span>{{ audioPlaying ? '关闭解说' : '开启解说' }}</span>
      </button>
      <button class="nav-btn" @click="takeScreenshot">
        <FontAwesomeIcon icon="camera" />
        <span>拍照</span>
      </button>
    </div>

    <!-- 展厅地图模态框 -->
    <div class="modal-overlay" v-if="showMap" @click="showMap = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>展厅地图</h3>
          <button class="close-btn" @click="showMap = false">
            <FontAwesomeIcon icon="times" />
          </button>
        </div>
        <div class="modal-body">
          <div class="exhibition-map">
            <!-- 地图内容 -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态管理
const activeControl = ref('move')
const viewCount = ref(2348)
const elapsedTime = ref(0)
const loading = ref(true)
const loadingProgress = ref(0)
const selectedArtifact = ref(null)
const showMap = ref(false)
const showGuide = ref(false)
const audioPlaying = ref(false)

// 标记点数据
const markers = reactive([
  { id: 1, name: '青铜鼎', x: 30, y: 40, era: '商代', material: '青铜',
    location: '河南安阳', dimensions: '高133cm',
    description: '商代青铜礼器代表作，纹饰精美，工艺精湛',
    image: '/images/bronze_ding.jpg' },
  { id: 2, name: '青铜尊', x: 50, y: 30, era: '商代', material: '青铜',
    location: '河南安阳', dimensions: '高45cm',
    description: '商代酒器，造型独特，工艺精良',
    image: '/images/bronze_zun.jpg' },
  { id: 3, name: '玉琮', x: 40, y: 60, era: '良渚文化', material: '玉石',
    location: '浙江余杭', dimensions: '高8.8cm',
    description: '良渚文化玉器，刻有神人兽面纹',
    image: '/images/jade_cong.jpg' }
])

// 定时器
let timer

onMounted(() => {
  // 模拟加载过程
  const loadInterval = setInterval(() => {
    loadingProgress.value += 10
    if (loadingProgress.value >= 100) {
      clearInterval(loadInterval)
      loading.value = false
    }
  }, 200)

  // 开始计时
  timer = setInterval(() => {
    elapsedTime.value++
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const setControl = (control) => {
  activeControl.value = control
}

const selectArtifact = (artifact) => {
  selectedArtifact.value = artifact
}

const viewDetail = (id) => {
  router.push(`/artifact/${id}`)
}

const startAIGuide = (id) => {
  router.push(`/ai-guide?artifact=${id}`)
}

const enterVR = () => {
  // 实际项目中这里会启动VR模式
  console.log('进入VR模式')
}

const toggleAudioGuide = () => {
  audioPlaying.value = !audioPlaying.value
}

const takeScreenshot = () => {
  // 实际项目中这里会截图
  console.log('拍照')
}

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.virtual-tour-view {
  height: 100vh;
  background: var(--bg-primary);
}

.tour-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: calc(100vh - 80px);
}

.tour-sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border-color);
  padding: 24px;
  overflow-y: auto;
}

.sidebar-header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.sidebar-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.exhibition-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 32px;
}

.exhibition-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.exhibition-item:hover {
  background: var(--surface-hover);
}

.exhibition-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border: 1px solid var(--primary);
}

.exhibition-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.exhibition-info {
  flex: 1;
}

.exhibition-info h4 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.exhibition-info p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.artifact-count {
  font-size: 11px;
  color: var(--text-secondary);
  background: var(--surface-hover);
  padding: 2px 8px;
  border-radius: 10px;
}

.current-location {
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 12px;
}

.current-location h4 {
  font-size: 14px;
  margin-bottom: 12px;
  color: var(--text-secondary);
}

.location-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.online-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background: var(--success);
  animation: pulse 2s infinite;
}

.tour-main {
  display: flex;
  flex-direction: column;
  position: relative;
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--surface);
  border-bottom: 1px solid var(--border-color);
}

.viewer-controls {
  display: flex;
  gap: 8px;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.control-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.control-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.viewer-stats {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
}

.scene-container {
  flex: 1;
  position: relative;
  background: linear-gradient(135deg, #667eea15, #764ba215);
}

.scene-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.artifact-markers {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.artifact-marker {
  position: absolute;
  cursor: pointer;
  transform: translate(-50%, -50%);
}

.marker-dot {
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  animation: pulse 2s infinite;
}

.marker-label {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.3s;
  pointer-events: none;
}

.artifact-marker:hover .marker-label {
  opacity: 1;
  top: 25px;
}

.scene-info {
  text-align: center;
  background: var(--surface);
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.scene-info h4 {
  font-size: 24px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.scene-info p {
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.loading-progress {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.progress-bar {
  width: 300px;
  height: 8px;
  background: var(--surface-hover);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  transition: width 0.3s;
}

.artifact-panel {
  position: absolute;
  right: 24px;
  bottom: 24px;
  width: 320px;
  background: var(--surface);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  transform: translateY(100%);
  opacity: 0;
  transition: all 0.3s;
}

.artifact-panel.active {
  transform: translateY(0);
  opacity: 1;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);
}

.panel-header h3 {
  font-size: 18px;
  margin: 0;
  color: var(--text-primary);
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--surface-hover);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.close-btn:hover {
  background: var(--surface);
  color: var(--text-primary);
}

.panel-content {
  padding: 24px;
}

.artifact-preview {
  position: relative;
  height: 180px;
  background: var(--bg-secondary);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

.preview-controls {
  position: absolute;
  bottom: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
}

.preview-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.preview-btn:hover {
  background: white;
  transform: scale(1.1);
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.info-row label {
  font-size: 14px;
  color: var(--text-secondary);
}

.info-row span {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.description {
  margin: 20px 0;
}

.description h4 {
  font-size: 16px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.description p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.artifact-actions {
  display: flex;
  gap: 8px;
}

.panel-empty {
  padding: 48px 24px;
  text-align: center;
  color: var(--text-secondary);
}

.panel-empty svg {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.quick-nav {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  background: var(--surface);
  padding: 8px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--surface-hover);
  border: none;
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: var(--primary);
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: var(--surface);
  border-radius: 24px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid var(--border-color);
}

.modal-body {
  padding: 24px;
}

.exhibition-map {
  height: 400px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

@media (max-width: 1024px) {
  .tour-container {
    grid-template-columns: 1fr;
  }

  .tour-sidebar {
    display: none;
  }

  .artifact-panel {
    width: 280px;
  }
}
</style>