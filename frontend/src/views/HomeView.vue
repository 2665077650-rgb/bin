<template>
  <div class="home-view">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h2 class="hero-title">穿越千年，触摸历史</h2>
        <p class="hero-subtitle">在数字世界中体验中华文明的璀璨与深邃</p>
        <div class="hero-actions">
          <button class="btn btn-primary btn-lg" @click="startVirtualTour">
            <FontAwesomeIcon icon="compass" />
            <span>开始探索</span>
          </button>
          <button class="btn btn-outline btn-lg">
            <FontAwesomeIcon icon="history" />
            <span>时间线浏览</span>
          </button>
        </div>
      </div>
      <div class="hero-image">
        <div class="floating-artifacts">
          <div class="artifact-1"></div>
          <div class="artifact-2"></div>
          <div class="artifact-3"></div>
        </div>
      </div>
    </section>

    <!-- 核心功能 -->
    <section class="core-features">
      <h3 class="section-title">核心探索方式</h3>
      <div class="features-grid">
        <div class="feature-card" @click="navigateTo('/virtual-tour')">
          <div class="feature-icon feature-icon-1">
            <FontAwesomeIcon icon="compass" />
          </div>
          <h4>3D虚拟展厅</h4>
          <p>360°沉浸式漫游，自由探索文物细节</p>
          <div class="feature-stats">
            <span>10+ 展厅</span>
            <span>•</span>
            <span>500+ 文物</span>
          </div>
        </div>

        <div class="feature-card" @click="navigateTo('/time-map')">
          <div class="feature-icon feature-icon-2">
            <FontAwesomeIcon icon="map" />
          </div>
          <h4>时空地图</h4>
          <p>可视化历史轨迹，追踪文物流转脉络</p>
          <div class="feature-stats">
            <span>8个朝代</span>
            <span>•</span>
            <span>100+ 遗址</span>
          </div>
        </div>

        <div class="feature-card" @click="navigateTo('/repair-lab')">
          <div class="feature-icon feature-icon-3">
            <FontAwesomeIcon icon="puzzle-piece" />
          </div>
          <h4>修复实验室</h4>
          <p>亲手拼接历史碎片，体验考古修复乐趣</p>
          <div class="feature-stats">
            <span>15+ 文物</span>
            <span>•</span>
            <span>3种难度</span>
          </div>
        </div>

        <div class="feature-card" @click="navigateTo('/ai-guide')">
          <div class="feature-icon feature-icon-4">
            <FontAwesomeIcon icon="robot" />
          </div>
          <h4>AI智能解说</h4>
          <p>24小时在线，有问必答的专业解说员</p>
          <div class="feature-stats">
            <span>中英双语</span>
            <span>•</span>
            <span>深度解读</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 热门展览 -->
    <section class="exhibitions-section">
      <div class="section-header">
        <h3 class="section-title">热门展览</h3>
        <button class="btn-link">查看全部 <FontAwesomeIcon icon="arrow-right" /></button>
      </div>
      <div class="exhibitions-grid">
        <div class="exhibition-card" v-for="exhibition in exhibitions" :key="exhibition.id">
          <div class="exhibition-image" :style="`background-image: url(${exhibition.image})`"></div>
          <div class="exhibition-content">
            <div class="exhibition-header">
              <span class="exhibition-tag" :class="exhibition.type">
                {{ exhibition.type === 'long-term' ? '常设展览' : '特展' }}
              </span>
              <span class="visitor-count">{{ exhibition.visitors }}</span>
            </div>
            <h4>{{ exhibition.title }}</h4>
            <p>{{ exhibition.description }}</p>
            <div class="exhibition-footer">
              <span class="date">{{ exhibition.date }}</span>
              <button class="btn btn-sm btn-outline" @click="visitExhibition(exhibition.id)">
                参观
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 镇馆之宝 -->
    <section class="treasure-section">
      <h3 class="section-title">镇馆之宝</h3>
      <div class="treasure-card">
        <div class="treasure-image">
          <div class="image-container">
            <div class="artifact-model"></div>
            <div class="model-controls">
              <button class="model-btn"><FontAwesomeIcon icon="expand" /></button>
              <button class="model-btn"><FontAwesomeIcon icon="rotate-left" /></button>
              <button class="model-btn"><FontAwesomeIcon icon="camera" /></button>
            </div>
          </div>
        </div>
        <div class="treasure-info">
          <div class="treasure-header">
            <h2>青铜鼎</h2>
            <div class="treasure-meta">
              <span class="era">商代晚期</span>
              <span class="location"><FontAwesomeIcon icon="map-marker-alt" /> 河南安阳</span>
            </div>
          </div>
          <div class="treasure-description">
            <p>商代青铜礼器代表作，通高133厘米，重832.84公斤，是目前已知中国古代最重的青铜器。</p>
            <p>器身饰有精美的饕餮纹、云雷纹和龙纹，体现了商代青铜铸造技术的最高水平。</p>
          </div>
          <div class="treasure-details">
            <div class="detail-item">
              <label>年代</label>
              <span>约公元前1250-1192年</span>
            </div>
            <div class="detail-item">
              <label>材质</label>
              <span>青铜（铜锡铅合金）</span>
            </div>
            <div class="detail-item">
              <label>出土时间</label>
              <span>1976年</span>
            </div>
            <div class="detail-item">
              <label>发掘地点</label>
              <span>安阳殷墟妇好墓</span>
            </div>
          </div>
          <div class="treasure-actions">
            <button class="btn btn-primary" @click="viewTreasureDetail">
              <FontAwesomeIcon icon="info-circle" />
              <span>详细解读</span>
            </button>
            <button class="btn btn-outline">
              <FontAwesomeIcon icon="share" />
              <span>分享</span>
            </button>
            <button class="btn btn-outline">
              <FontAwesomeIcon icon="heart" />
              <span>收藏</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 近期活动 -->
    <section class="activities-section">
      <h3 class="section-title">近期活动</h3>
      <div class="activities-grid">
        <div class="activity-card">
          <div class="activity-date">
            <span class="day">15</span>
            <span class="month">6月</span>
          </div>
          <div class="activity-content">
            <h4>线上文物修复工作坊</h4>
            <p>学习青铜器修复技术，亲手体验文物修复过程</p>
            <div class="activity-meta">
              <span><FontAwesomeIcon icon="users" /> 剩余12个名额</span>
              <span><FontAwesomeIcon icon="clock" /> 14:00-16:00</span>
            </div>
          </div>
          <button class="btn btn-primary btn-sm">报名参加</button>
        </div>
        <!-- 更多活动卡片 -->
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchExhibitions, fetchTreasure } from '@/api/museum'

const router = useRouter()

const exhibitions = ref([
  {
    id: 1,
    title: '商周青铜器',
    description: '展示商周时期青铜器的精湛工艺与文化内涵',
    type: 'long-term',
    visitors: '2.3万参观',
    date: '常设展览',
    image: '/images/exhibition1.jpg'
  },
  {
    id: 2,
    title: '唐宋瓷器',
    description: '唐宋时期瓷器艺术的巅峰之作，展现东方美学',
    type: 'temporary',
    visitors: '1.8万参观',
    date: '2024.01-06',
    image: '/images/exhibition2.jpg'
  },
  {
    id: 3,
    title: '古代玉器珍藏',
    description: '从新石器时代到明清的玉器发展历程',
    type: 'long-term',
    visitors: '3.1万参观',
    date: '常设展览',
    image: '/images/exhibition3.jpg'
  }
])

const navigateTo = (path) => {
  router.push(path)
}

const startVirtualTour = () => {
  router.push('/virtual-tour')
}

const visitExhibition = (id) => {
  router.push(`/exhibition/${id}`)
}

const viewTreasureDetail = () => {
  router.push('/artifact/1')
}

onMounted(async () => {
  try {
    const data = await fetchExhibitions()
    exhibitions.value = data
  } catch (error) {
    console.error('获取展览数据失败:', error)
  }
})
</script>

<style scoped>
.home-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
  margin-bottom: 80px;
  padding: 48px 0;
}

.hero-content {
  animation: slideInLeft 0.8s ease;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 32px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.hero-image {
  position: relative;
  height: 400px;
  animation: slideInRight 0.8s ease;
}

.floating-artifacts {
  position: relative;
  width: 100%;
  height: 100%;
}

.artifact-1,
.artifact-2,
.artifact-3 {
  position: absolute;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 16px;
  animation: float 6s ease-in-out infinite;
}

.artifact-1 {
  width: 120px;
  height: 160px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.artifact-2 {
  width: 100px;
  height: 100px;
  top: 50%;
  right: 20%;
  border-radius: 50%;
  animation-delay: 2s;
}

.artifact-3 {
  width: 140px;
  height: 100px;
  bottom: 10%;
  left: 30%;
  animation-delay: 4s;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 32px;
  color: var(--text-primary);
}

.core-features {
  margin-bottom: 80px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.feature-card {
  background: var(--surface);
  border-radius: 16px;
  padding: 32px;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-8px);
  border-color: var(--primary);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.feature-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  font-size: 28px;
  color: white;
}

.feature-icon-1 {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.feature-icon-2 {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.feature-icon-3 {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.feature-icon-4 {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.feature-card h4 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  margin-bottom: 16px;
  line-height: 1.6;
}

.feature-stats {
  display: flex;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.btn-link {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: var(--primary);
  font-size: 16px;
  cursor: pointer;
  padding: 0;
}

.exhibitions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 80px;
}

.exhibition-card {
  background: var(--surface);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.exhibition-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.exhibition-image {
  height: 200px;
  background-size: cover;
  background-position: center;
}

.exhibition-content {
  padding: 24px;
}

.exhibition-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.exhibition-tag {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.exhibition-tag.long-term {
  background: #e3f2fd;
  color: #1976d2;
}

.exhibition-tag.temporary {
  background: #fff3e0;
  color: #f57c00;
}

.visitor-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.exhibition-content h4 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.exhibition-content p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 20px;
}

.exhibition-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exhibition-footer .date {
  font-size: 14px;
  color: var(--text-secondary);
}

.treasure-section {
  margin-bottom: 80px;
}

.treasure-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  background: var(--surface);
  border-radius: 24px;
  padding: 48px;
  border: 1px solid var(--border-color);
}

.treasure-image {
  position: relative;
}

.image-container {
  position: relative;
  height: 400px;
  background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
  border-radius: 16px;
  overflow: hidden;
}

.artifact-model {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 250px;
  background: linear-gradient(45deg, #cd7f32, #b87333, #aa6c39);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.model-controls {
  position: absolute;
  bottom: 16px;
  right: 16px;
  display: flex;
  gap: 8px;
}

.model-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.model-btn:hover {
  background: var(--surface-hover);
}

.treasure-info {
  display: flex;
  flex-direction: column;
}

.treasure-header {
  margin-bottom: 24px;
}

.treasure-header h2 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.treasure-meta {
  display: flex;
  gap: 16px;
  font-size: 16px;
  color: var(--text-secondary);
}

.era {
  background: var(--surface-hover);
  padding: 4px 12px;
  border-radius: 12px;
}

.location {
  display: flex;
  align-items: center;
  gap: 4px;
}

.treasure-description {
  margin-bottom: 32px;
}

.treasure-description p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 12px;
}

.treasure-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.detail-item span {
  font-size: 14px;
  color: var(--text-primary);
  font-weight: 500;
}

.treasure-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.activity-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--surface);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid var(--border-color);
}

.activity-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
}

.activity-date .day {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary);
}

.activity-date .month {
  font-size: 14px;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.activity-content p {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.5;
}

.activity-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--text-secondary);
}

.activity-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 12px;
  border: 2px solid transparent;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  border: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.btn-outline {
  background: transparent;
  border-color: var(--border-color);
  color: var(--text-primary);
}

.btn-outline:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.btn-lg {
  padding: 16px 32px;
  font-size: 18px;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .hero-title {
    font-size: 36px;
  }

  .treasure-card {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  .features-grid,
  .exhibitions-grid {
    grid-template-columns: 1fr;
  }
}
</style>