<template>
  <div class="time-map-view">
    <!-- 时间轴控制栏 -->
    <div class="timeline-controls">
      <div class="controls-left">
        <button class="control-btn" @click="zoomIn">
          <FontAwesomeIcon icon="plus" />
        </button>
        <button class="control-btn" @click="zoomOut">
          <FontAwesomeIcon icon="minus" />
        </button>
        <button class="control-btn" @click="resetView">
          <FontAwesomeIcon icon="expand-arrows-alt" />
        </button>
      </div>

      <div class="era-selector">
        <button v-for="era in eras" :key="era.name"
                class="era-btn" :class="{active: activeEra === era.name}"
                @click="selectEra(era)">
          {{ era.name }}
        </button>
      </div>

      <div class="controls-right">
        <div class="year-display">
          <span class="current-year">{{ currentYear }}</span>
          <span v-if="activeEra" class="era-name">{{ activeEra }}</span>
        </div>
        <div class="slider-container">
          <input type="range" v-model="timelinePosition" min="0" max="100"
                 class="timeline-slider" @input="onTimelineChange">
          <div class="slider-marks">
            <span v-for="mark in timelineMarks" :key="mark.year"
                  :style="{left: mark.position + '%'}"
                  @click="jumpToYear(mark.year)">
              {{ mark.year > 0 ? mark.year + '年' : `${Math.abs(mark.year)}年` }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主地图区域 -->
    <div class="map-container">
      <div class="map-view" ref="mapView">
        <!-- 地图图层 -->
        <div class="map-layer base-map"></div>
        <div class="map-layer artifact-layer">
          <div v-for="artifact in visibleArtifacts" :key="artifact.id"
               class="map-marker" :class="artifact.type"
               :style="{
                 left: artifact.x + '%',
                 top: artifact.y + '%'
               }"
               @click="selectArtifact(artifact)">
            <div class="marker-pin"></div>
            <div class="marker-tooltip">
              <div class="tooltip-header">
                <h4>{{ artifact.name }}</h4>
                <span class="era-badge">{{ artifact.era }}</span>
              </div>
              <p class="tooltip-desc">{{ artifact.description }}</p>
              <div class="tooltip-meta">
                <span><FontAwesomeIcon icon="map-marker-alt" /> {{ artifact.location }}</span>
                <span><FontAwesomeIcon icon="box" /> {{ artifact.material }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 历史事件图层 -->
        <div class="map-layer event-layer">
          <div v-for="event in visibleEvents" :key="event.id"
               class="event-marker" :style="{
                 left: event.x + '%',
                 top: event.y + '%'
               }">
            <div class="event-icon" :class="event.type">
              <FontAwesomeIcon :icon="getEventIcon(event.type)" />
            </div>
          </div>
        </div>

        <!-- 迁徙路线 -->
        <div class="map-layer route-layer">
          <svg class="route-svg">
            <path v-for="route in visibleRoutes" :key="route.id"
                  :d="route.path" class="route-path" />
          </svg>
        </div>
      </div>

      <!-- 右侧信息面板 -->
      <div class="info-panel" :class="{collapsed: panelCollapsed}">
        <button class="panel-toggle" @click="panelCollapsed = !panelCollapsed">
          <FontAwesomeIcon :icon="panelCollapsed ? 'chevron-left' : 'chevron-right'" />
        </button>

        <div class="panel-content">
          <div class="panel-section artifact-info" v-if="selectedArtifact">
            <div class="section-header">
              <h3>{{ selectedArtifact.name }}</h3>
              <button class="close-btn" @click="selectedArtifact = null">
                <FontAwesomeIcon icon="times" />
              </button>
            </div>

            <div class="artifact-gallery">
              <div class="main-image" :style="`background-image: url(${selectedArtifact.image})`"></div>
              <div class="image-thumbnails">
                <div v-for="(img, idx) in selectedArtifact.images" :key="idx"
                     class="thumbnail" :style="`background-image: url(${img})`"></div>
              </div>
            </div>

            <div class="artifact-details">
              <div class="detail-grid">
                <div class="detail-item">
                  <label><FontAwesomeIcon icon="calendar" /> 年代</label>
                  <span>{{ selectedArtifact.era }}</span>
                </div>
                <div class="detail-item">
                  <label><FontAwesomeIcon icon="map-marker-alt" /> 出土地</label>
                  <span>{{ selectedArtifact.location }}</span>
                </div>
                <div class="detail-item">
                  <label><FontAwesomeIcon icon="box" /> 材质</label>
                  <span>{{ selectedArtifact.material }}</span>
                </div>
                <div class="detail-item">
                  <label><FontAwesomeIcon icon="ruler" /> 尺寸</label>
                  <span>{{ selectedArtifact.dimensions }}</span>
                </div>
              </div>

              <div class="artifact-description">
                <h4>文物介绍</h4>
                <p>{{ selectedArtifact.description }}</p>
              </div>

              <div class="artifact-history">
                <h4><FontAwesomeIcon icon="route" /> 流转历史</h4>
                <div class="history-timeline">
                  <div v-for="event in selectedArtifact.history" :key="event.year"
                       class="history-event">
                    <div class="event-year">{{ event.year }}</div>
                    <div class="event-content">
                      <strong>{{ event.title }}</strong>
                      <p>{{ event.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="artifact-actions">
              <button class="btn btn-primary" @click="viewIn3D(selectedArtifact.id)">
                <FontAwesomeIcon icon="cube" />
                <span>3D查看</span>
              </button>
              <button class="btn btn-outline" @click="showInTimeline(selectedArtifact)">
                <FontAwesomeIcon icon="history" />
                <span>时间轴定位</span>
              </button>
            </div>
          </div>

          <div class="panel-section filter-panel" v-else>
            <h3>筛选条件</h3>

            <div class="filter-group">
              <h4><FontAwesomeIcon icon="filter" /> 文物类型</h4>
              <div class="filter-chips">
                <button v-for="type in artifactTypes" :key="type"
                        class="filter-chip" :class="{active: filters.types.includes(type)}"
                        @click="toggleFilter('types', type)">
                  {{ type }}
                </button>
              </div>
            </div>

            <div class="filter-group">
              <h4><FontAwesomeIcon icon="calendar" /> 年代范围</h4>
              <div class="year-range">
                <span>{{ filters.yearRange[0] }}</span>
                <input type="range" v-model="filters.yearRange[0]" :min="minYear" :max="maxYear">
                <input type="range" v-model="filters.yearRange[1]" :min="minYear" :max="maxYear">
                <span>{{ filters.yearRange[1] }}</span>
              </div>
            </div>

            <div class="filter-group">
              <h4><FontAwesomeIcon icon="map-marker-alt" /> 地区分布</h4>
              <div class="region-list">
                <button v-for="region in regions" :key="region"
                        class="region-btn" :class="{active: filters.regions.includes(region)}"
                        @click="toggleFilter('regions', region)">
                  {{ region }}
                </button>
              </div>
            </div>

            <div class="filter-actions">
              <button class="btn btn-outline" @click="resetFilters">
                <FontAwesomeIcon icon="redo" />
                <span>重置筛选</span>
              </button>
              <button class="btn btn-primary" @click="applyFilters">
                <FontAwesomeIcon icon="check" />
                <span>应用筛选</span>
              </button>
            </div>
          </div>

          <div class="panel-section stats-panel">
            <h3>数据统计</h3>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-value">{{ totalArtifacts }}</div>
                <div class="stat-label">文物总数</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ visibleArtifacts.length }}</div>
                <div class="stat-label">当前显示</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ eras.length }}</div>
                <div class="stat-label">历史时期</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{{ regions.length }}</div>
                <div class="stat-label">分布地区</div>
              </div>
            </div>

            <div class="stat-chart">
              <h4>文物年代分布</h4>
              <div class="chart-bars">
                <div v-for="era in eraDistribution" :key="era.name"
                     class="chart-bar" :style="{height: era.count * 2 + 'px'}">
                  <span class="bar-label">{{ era.name }}</span>
                  <span class="bar-value">{{ era.count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部时间线 -->
    <div class="bottom-timeline">
      <div class="timeline-track">
        <div class="timeline-progress" :style="{width: timelinePosition + '%'}"></div>
        <div class="timeline-marks">
          <div v-for="mark in detailedMarks" :key="mark.year"
               class="timeline-mark" :style="{left: mark.position + '%'}"
               @click="jumpToYear(mark.year)">
            <div class="mark-year">{{ formatYear(mark.year) }}</div>
            <div class="mark-events">
              <div v-for="event in mark.events" :key="event.id"
                   class="mark-event" :class="event.type">
                {{ event.title }}
              </div>
            </div>
          </div>
        </div>
        <div class="timeline-pointer" :style="{left: timelinePosition + '%'}">
          <div class="pointer-dot"></div>
          <div class="pointer-year">{{ formatYear(currentYearValue) }}</div>
        </div>
      </div>
    </div>

    <!-- 地图控制工具 -->
    <div class="map-tools">
      <div class="tools-group">
        <button class="tool-btn" @click="toggleLayer('artifacts')"
                :class="{active: layers.artifacts}">
          <FontAwesomeIcon icon="monument" />
          <span>文物</span>
        </button>
        <button class="tool-btn" @click="toggleLayer('events')"
                :class="{active: layers.events}">
          <FontAwesomeIcon icon="landmark" />
          <span>事件</span>
        </button>
        <button class="tool-btn" @click="toggleLayer('routes')"
                :class="{active: layers.routes}">
          <FontAwesomeIcon icon="route" />
          <span>路线</span>
        </button>
      </div>

      <div class="tools-group">
        <button class="tool-btn">
          <FontAwesomeIcon icon="search" />
          <span>搜索</span>
        </button>
        <button class="tool-btn" @click="exportMap">
          <FontAwesomeIcon icon="download" />
          <span>导出</span>
        </button>
        <button class="tool-btn" @click="toggleHeatmap">
          <FontAwesomeIcon icon="fire" />
          <span>热力图</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 状态管理
const mapView = ref(null)
const panelCollapsed = ref(false)
const activeEra = ref(null)
const timelinePosition = ref(50)
const selectedArtifact = ref(null)
const showHeatmap = ref(false)

// 地图数据
const eras = ref([
  { name: '新石器时代', start: -8000, end: -2000, color: '#FBBF24' },
  { name: '夏商周', start: -2070, end: -256, color: '#F59E0B' },
  { name: '秦汉', start: -221, end: 220, color: '#10B981' },
  { name: '魏晋南北朝', start: 220, end: 589, color: '#3B82F6' },
  { name: '隋唐', start: 581, end: 907, color: '#8B5CF6' },
  { name: '宋元', start: 960, end: 1368, color: '#EC4899' },
  { name: '明清', start: 1368, end: 1912, color: '#EF4444' },
  { name: '近现代', start: 1912, end: 2024, color: '#6B7280' }
])

const filters = reactive({
  types: ['青铜', '玉石', '陶瓷', '书画'],
  yearRange: [-8000, 2024],
  regions: ['华北', '华东', '华南', '西南', '西北', '东北']
})

const layers = reactive({
  artifacts: true,
  events: true,
  routes: true
})

// 文物数据
const artifacts = ref([
  {
    id: 1,
    name: '青铜鼎',
    era: '商代',
    location: '河南安阳',
    material: '青铜',
    description: '商代青铜礼器代表作',
    x: 30,
    y: 40,
    type: 'bronze',
    images: ['/images/bronze_ding_1.jpg', '/images/bronze_ding_2.jpg'],
    dimensions: '高133cm，重832.84kg',
    history: [
      { year: -1250, title: '铸造', description: '在商代晚期铸造完成' },
      { year: -1200, title: '使用', description: '用于祭祀活动' },
      { year: 1928, title: '出土', description: '安阳殷墟发掘出土' }
    ]
  },
  // 更多文物数据...
])

const regions = ref(['华北', '华东', '华南', '西南', '西北', '东北'])
const artifactTypes = ref(['青铜', '玉石', '陶瓷', '书画', '金银器', '漆木器'])

// 计算属性
const currentYearValue = computed(() => {
  const minYear = -8000
  const maxYear = 2024
  return Math.round(minYear + (maxYear - minYear) * timelinePosition.value / 100)
})

const currentYear = computed(() => {
  const year = currentYearValue.value
  return year >= 0 ? `${year}年` : `${Math.abs(year)}年`
})

const visibleArtifacts = computed(() => {
  return artifacts.value.filter(artifact => {
    // 根据筛选条件过滤
    const inYearRange = artifact.year >= filters.yearRange[0] &&
                       artifact.year <= filters.yearRange[1]
    const hasType = filters.types.includes(artifact.material)
    return inYearRange && hasType && layers.artifacts
  })
})

const totalArtifacts = computed(() => artifacts.value.length)

const eraDistribution = computed(() => {
  return eras.value.map(era => ({
    name: era.name,
    count: artifacts.value.filter(a => a.year >= era.start && a.year <= era.end).length
  }))
})

// 时间轴标记
const timelineMarks = computed(() => [
  { year: -8000, position: 0 },
  { year: -2000, position: 25 },
  { year: 0, position: 50 },
  { year: 1000, position: 75 },
  { year: 2024, position: 100 }
])

const detailedMarks = computed(() => {
  const marks = []
  for (let year = -8000; year <= 2024; year += 500) {
    marks.push({
      year,
      position: ((year + 8000) / 10024) * 100,
      events: getEventsForYear(year)
    })
  }
  return marks
})

// 方法
const zoomIn = () => {
  console.log('放大')
}

const zoomOut = () => {
  console.log('缩小')
}

const resetView = () => {
  timelinePosition.value = 50
  selectedArtifact.value = null
}

const selectEra = (era) => {
  activeEra.value = era.name
  timelinePosition.value = ((era.start + 8000) / 10024) * 100
}

const onTimelineChange = () => {
  // 更新时间轴位置
}

const jumpToYear = (year) => {
  timelinePosition.value = ((year + 8000) / 10024) * 100
}

const selectArtifact = (artifact) => {
  selectedArtifact.value = artifact
  panelCollapsed.value = false
}

const viewIn3D = (id) => {
  router.push(`/virtual-tour?artifact=${id}`)
}

const showInTimeline = (artifact) => {
  // 在时间轴上高亮显示
}

const toggleFilter = (filterType, value) => {
  const index = filters[filterType].indexOf(value)
  if (index > -1) {
    filters[filterType].splice(index, 1)
  } else {
    filters[filterType].push(value)
  }
}

const resetFilters = () => {
  filters.types = [...artifactTypes.value]
  filters.yearRange = [-8000, 2024]
  filters.regions = [...regions.value]
}

const applyFilters = () => {
  // 应用筛选条件
}

const toggleLayer = (layer) => {
  layers[layer] = !layers[layer]
}

const exportMap = () => {
  console.log('导出地图')
}

const toggleHeatmap = () => {
  showHeatmap.value = !showHeatmap.value
}

const getEventIcon = (type) => {
  const icons = {
    political: 'landmark',
    cultural: 'palette',
    economic: 'coins',
    military: 'shield-alt'
  }
  return icons[type] || 'history'
}

const getEventsForYear = (year) => {
  // 获取该年份的事件
  return []
}

const formatYear = (year) => {
  return year >= 0 ? `${year}年` : `${Math.abs(year)}年`
}

onMounted(() => {
  // 初始化地图
})
</script>

<style scoped>
.time-map-view {
  height: 100vh;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
}

.timeline-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--surface);
  border-bottom: 1px solid var(--border-color);
  height: 80px;
}

.controls-left {
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
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
  border-color: var(--primary);
}

.era-selector {
  display: flex;
  gap: 4px;
}

.era-btn {
  padding: 8px 16px;
  border: none;
  background: var(--surface-hover);
  color: var(--text-secondary);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.era-btn.active {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
}

.controls-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  min-width: 300px;
}

.year-display {
  display: flex;
  align-items: center;
  gap: 12px;
}

.current-year {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary);
}

.era-name {
  background: var(--surface-hover);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
}

.slider-container {
  position: relative;
  width: 100%;
}

.timeline-slider {
  width: 100%;
  height: 8px;
  background: var(--surface-hover);
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
}

.timeline-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  background: var(--primary);
  border-radius: 50%;
  cursor: pointer;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.slider-marks {
  position: absolute;
  top: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
}

.slider-marks span {
  position: absolute;
  transform: translateX(-50%);
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.3s;
}

.slider-marks span:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.map-container {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
}

.map-view {
  flex: 1;
  position: relative;
  background: linear-gradient(135deg, #667eea10, #764ba210);
}

.map-layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.base-map {
  background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
}

.map-marker {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
  z-index: 10;
}

.marker-pin {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 50% 50% 50% 0;
  transform: rotate(-45deg);
  position: relative;
}

.marker-pin::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: white;
  border-radius: 50%;
}

.map-marker.bronze .marker-pin {
  background: linear-gradient(135deg, #cd7f32, #b87333);
}

.map-marker.jade .marker-pin {
  background: linear-gradient(135deg, #00b894, #00a085);
}

.map-marker.ceramic .marker-pin {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
}

.marker-tooltip {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  width: 240px;
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s;
  z-index: 20;
}

.map-marker:hover .marker-tooltip {
  opacity: 1;
  top: 30px;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.tooltip-header h4 {
  font-size: 16px;
  margin: 0;
  color: var(--text-primary);
}

.era-badge {
  background: var(--surface-hover);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  color: var(--text-secondary);
}

.tooltip-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  line-height: 1.4;
}

.tooltip-meta {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-secondary);
}

.tooltip-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.event-marker {
  position: absolute;
  transform: translate(-50%, -50%);
}

.event-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
}

.event-icon.political {
  background: #ef4444;
}

.event-icon.cultural {
  background: #3b82f6;
}

.event-icon.economic {
  background: #10b981;
}

.route-svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.route-path {
  fill: none;
  stroke: var(--primary);
  stroke-width: 2;
  stroke-dasharray: 5,5;
  opacity: 0.6;
}

.info-panel {
  position: relative;
  width: 360px;
  background: var(--surface);
  border-left: 1px solid var(--border-color);
  transition: transform 0.3s;
  overflow-y: auto;
}

.info-panel.collapsed {
  transform: translateX(100%);
}

.panel-toggle {
  position: absolute;
  left: -40px;
  top: 20px;
  width: 40px;
  height: 40px;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-right: none;
  border-radius: 8px 0 0 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
}

.panel-content {
  padding: 24px;
}

.panel-section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 20px;
  margin: 0;
  color: var(--text-primary);
}

.artifact-gallery {
  margin-bottom: 20px;
}

.main-image {
  height: 200px;
  background: var(--bg-secondary);
  border-radius: 12px;
  margin-bottom: 12px;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

.image-thumbnails {
  display: flex;
  gap: 8px;
}

.thumbnail {
  width: 60px;
  height: 60px;
  background: var(--bg-secondary);
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  cursor: pointer;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-item span {
  font-size: 14px;
  color: var(--text-primary);
}

.artifact-description {
  margin-bottom: 24px;
}

.artifact-description h4 {
  font-size: 16px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.artifact-description p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.artifact-history {
  margin-bottom: 24px;
}

.artifact-history h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.history-timeline {
  position: relative;
  padding-left: 20px;
}

.history-timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border-color);
}

.history-event {
  position: relative;
  margin-bottom: 16px;
}

.history-event::before {
  content: '';
  position: absolute;
  left: -24px;
  top: 8px;
  width: 8px;
  height: 8px;
  background: var(--primary);
  border-radius: 50%;
}

.event-year {
  font-size: 12px;
  color: var(--primary);
  font-weight: 600;
  margin-bottom: 4px;
}

.event-content strong {
  display: block;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.event-content p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.artifact-actions {
  display: flex;
  gap: 8px;
}

.filter-panel h3 {
  margin-bottom: 24px;
}

.filter-group {
  margin-bottom: 24px;
}

.filter-group h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-chip {
  padding: 6px 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.filter-chip.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.year-range {
  display: flex;
  align-items: center;
  gap: 12px;
}

.year-range span {
  font-size: 12px;
  color: var(--text-secondary);
  min-width: 60px;
}

.year-range input[type="range"] {
  flex: 1;
}

.region-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.region-btn {
  padding: 6px 12px;
  background: var(--surface-hover);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.region-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.filter-actions {
  display: flex;
  gap: 8px;
}

.stats-panel h3 {
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: 12px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.stat-chart h4 {
  font-size: 14px;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 120px;
  padding: 0 8px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, var(--primary), var(--secondary));
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 20px;
}

.bar-label {
  position: absolute;
  bottom: -20px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 10px;
  color: var(--text-secondary);
  transform: rotate(-45deg);
  transform-origin: top left;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 10px;
  color: var(--text-primary);
}

.bottom-timeline {
  height: 120px;
  background: var(--surface);
  border-top: 1px solid var(--border-color);
  padding: 16px 24px;
}

.timeline-track {
  position: relative;
  height: 4px;
  background: var(--surface-hover);
  border-radius: 2px;
  margin-top: 40px;
}

.timeline-progress {
  position: absolute;
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 2px;
}

.timeline-marks {
  position: absolute;
  top: -40px;
  left: 0;
  right: 0;
}

.timeline-mark {
  position: absolute;
  transform: translateX(-50%);
  cursor: pointer;
}

.mark-year {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
  white-space: nowrap;
}

.mark-events {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mark-event {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.mark-event.political {
  background: #fee2e2;
  color: #dc2626;
}

.mark-event.cultural {
  background: #dbeafe;
  color: #2563eb;
}

.timeline-pointer {
  position: absolute;
  top: -8px;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pointer-dot {
  width: 16px;
  height: 16px;
  background: var(--primary);
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.pointer-year {
  margin-top: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--primary);
  background: white;
  padding: 2px 8px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.map-tools {
  position: absolute;
  right: 24px;
  bottom: 150px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tools-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: var(--surface);
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: none;
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.tool-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.tool-btn.active {
  background: var(--primary);
  color: white;
}

@media (max-width: 1200px) {
  .info-panel {
    width: 300px;
  }

  .timeline-controls {
    flex-direction: column;
    gap: 16px;
    height: auto;
    padding: 16px;
  }

  .controls-right {
    width: 100%;
  }
}
</style>