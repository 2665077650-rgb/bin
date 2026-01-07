<template>
  <div class="hello-world">
    <h1>{{ msg }}</h1>
    <p>欢迎来到时空博物馆系统</p>
    <div class="features">
      <div v-for="feature in features" :key="feature.id" class="feature-card">
        <div class="feature-icon">
          <FontAwesomeIcon :icon="feature.icon" />
        </div>
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  msg: {
    type: String,
    default: '时空博物馆'
  }
})

const features = ref([
  {
    id: 1,
    title: '3D虚拟展厅',
    description: '沉浸式体验，自由探索文物',
    icon: 'vr-cardboard'
  },
  {
    id: 2,
    title: '时空地图',
    description: '可视化历史轨迹和文物流转',
    icon: 'map-marked-alt'
  },
  {
    id: 3,
    title: '虚拟修复',
    description: '亲手拼接历史碎片',
    icon: 'puzzle-piece'
  },
  {
    id: 4,
    title: 'AI解说',
    description: '智能问答，深度解读',
    icon: 'robot'
  }
])
</script>

<style scoped>
.hello-world {
  text-align: center;
  padding: 2rem;
}

h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p {
  font-size: 1.2rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: var(--surface);
  padding: 2rem;
  border-radius: 1rem;
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-0.5rem);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  font-size: 2.5rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.feature-card p {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 0;
}
</style>