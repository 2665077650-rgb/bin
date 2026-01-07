<template>
  <div class="repair-lab-view">
    <!-- 实验室标题 -->
    <div class="lab-header">
      <div class="header-content">
        <h1><FontAwesomeIcon icon="flask" /> 虚拟修复实验室</h1>
        <p class="subtitle">亲手拼接历史碎片，让文物重焕新生</p>
      </div>
      <div class="user-stats">
        <div class="stat-item">
          <div class="stat-value">{{ userStats.completed }}</div>
          <div class="stat-label">已修复文物</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userStats.score }}</div>
          <div class="stat-label">修复积分</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userStats.rank }}</div>
          <div class="stat-label">排名</div>
        </div>
      </div>
    </div>

    <div class="lab-container">
      <!-- 左侧文物选择 -->
      <div class="artifact-selection">
        <div class="selection-header">
          <h3><FontAwesomeIcon icon="puzzle-piece" /> 选择修复文物</h3>
          <div class="difficulty-selector">
            <span class="difficulty-label">难度：</span>
            <select v-model="selectedDifficulty" @change="filterArtifacts">
              <option value="all">全部</option>
              <option value="easy">简单</option>
              <option value="medium">中等</option>
              <option value="hard">困难</option>
            </select>
          </div>
        </div>

        <div class="artifact-list">
          <div v-for="artifact in filteredArtifacts" :key="artifact.id"
               class="artifact-card" :class="{selected: selectedArtifact?.id === artifact.id}"
               @click="selectArtifact(artifact)">
            <div class="artifact-image" :style="`background-image: url(${artifact.image})`">
              <div class="artifact-status" :class="artifact.status">
                {{ artifact.status === 'completed' ? '已修复' : '待修复' }}
              </div>
              <div class="artifact-difficulty" :class="artifact.difficulty">
                {{ artifact.difficulty }}
              </div>
            </div>
            <div class="artifact-info">
              <h4>{{ artifact.name }}</h4>
              <div class="artifact-meta">
                <span class="era">{{ artifact.era }}</span>
                <span class="material">{{ artifact.material }}</span>
              </div>
              <div class="artifact-stats">
                <span><FontAwesomeIcon icon="puzzle-piece" /> {{ artifact.pieceCount }}碎片</span>
                <span><FontAwesomeIcon icon="clock" /> {{ artifact.avgTime }}分钟</span>
              </div>
            </div>
          </div>
        </div>

        <div class="user-achievements">
          <h4><FontAwesomeIcon icon="trophy" /> 修复成就</h4>
          <div class="achievements-list">
            <div v-for="achievement in achievements" :key="achievement.id"
                 class="achievement-item" :class="{unlocked: achievement.unlocked}">
              <div class="achievement-icon">
                <FontAwesomeIcon :icon="achievement.icon" />
              </div>
              <div class="achievement-info">
                <h5>{{ achievement.name }}</h5>
                <p>{{ achievement.description }}</p>
                <div class="achievement-progress" v-if="!achievement.unlocked">
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{width: achievement.progress + '%'}"></div>
                  </div>
                  <span>{{ achievement.progress }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间修复工作台 -->
      <div class="repair-workbench">
        <div class="workbench-header">
          <div class="artifact-info" v-if="selectedArtifact">
            <h3>{{ selectedArtifact.name }}</h3>
            <div class="artifact-details">
              <span class="era">{{ selectedArtifact.era }}</span>
              <span class="material">{{ selectedArtifact.material }}</span>
              <span class="difficulty" :class="selectedArtifact.difficulty">
                {{ selectedArtifact.difficulty }}
              </span>
            </div>
          </div>
          <div class="workbench-controls">
            <button class="control-btn" @click="showHint">
              <FontAwesomeIcon icon="lightbulb" />
              <span>提示</span>
            </button>
            <button class="control-btn" @click="resetPuzzle">
              <FontAwesomeIcon icon="undo" />
              <span>重置</span>
            </button>
            <button class="control-btn" @click="toggleGrid">
              <FontAwesomeIcon icon="th" />
              <span>{{ showGrid ? '隐藏网格' : '显示网格' }}</span>
            </button>
            <button class="control-btn" @click="toggleMagnetism">
              <FontAwesomeIcon :icon="magnetismEnabled ? 'magnet' : 'magnet'" />
              <span>{{ magnetismEnabled ? '关闭磁吸' : '开启磁吸' }}</span>
            </button>
          </div>
        </div>

        <div class="workbench-container">
          <!-- 参考图 -->
          <div class="reference-view">
            <div class="reference-header">
              <h4><FontAwesomeIcon icon="image" /> 参考图</h4>
              <div class="reference-controls">
                <button class="ref-btn" @click="toggleReference">
                  <FontAwesomeIcon :icon="referenceVisible ? 'eye' : 'eye-slash'" />
                </button>
                <button class="ref-btn" @click="adjustReferenceOpacity(-0.1)">
                  <FontAwesomeIcon icon="minus" />
                </button>
                <div class="opacity-display">{{ Math.round(referenceOpacity * 100) }}%</div>
                <button class="ref-btn" @click="adjustReferenceOpacity(0.1)">
                  <FontAwesomeIcon icon="plus" />
                </button>
              </div>
            </div>
            <div class="reference-image" :style="{
              backgroundImage: `url(${selectedArtifact?.referenceImage})`,
              opacity: referenceOpacity
            }"></div>
          </div>

          <!-- 拼图区域 -->
          <div class="puzzle-area" ref="puzzleArea"
               @dragover.prevent @drop="onDrop"
               :class="{grid: showGrid}">
            <!-- 网格 -->
            <div class="grid-overlay" v-if="showGrid">
              <div v-for="i in gridSize" :key="i" class="grid-line"></div>
            </div>

            <!-- 拼图碎片 -->
            <div v-for="piece in puzzlePieces" :key="piece.id"
                 class="puzzle-piece" :class="{placed: piece.placed}"
                 :style="{
                   left: piece.x + 'px',
                   top: piece.y + 'px',
                   width: pieceSize + 'px',
                   height: pieceSize + 'px',
                   backgroundImage: `url(${selectedArtifact?.puzzleImage})`,
                   backgroundPosition: piece.bgPosition
                 }"
                 draggable="true"
                 @dragstart="onDragStart(piece.id)"
                 @touchstart="onTouchStart(piece.id, $event)">
              <div class="piece-id">{{ piece.id }}</div>
              <div class="piece-hint" v-if="piece.hint">
                <FontAwesomeIcon icon="lightbulb" />
              </div>
            </div>

            <!-- 放置提示 -->
            <div class="drop-zones">
              <div v-for="zone in dropZones" :key="zone.id"
                   class="drop-zone" :style="{
                     left: zone.x + 'px',
                     top: zone.y + 'px',
                     width: pieceSize + 'px',
                     height: pieceSize + 'px'
                   }"></div>
            </div>

            <!-- 进度显示 -->
            <div class="puzzle-progress">
              <div class="progress-info">
                <span>{{ placedPiecesCount }} / {{ totalPiecesCount }} 碎片</span>
                <span>{{ Math.round((placedPiecesCount / totalPiecesCount) * 100) }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{width: (placedPiecesCount / totalPiecesCount) * 100 + '%'}"></div>
              </div>
            </div>
          </div>

          <!-- 工具面板 -->
          <div class="tool-panel">
            <div class="tools-header">
              <h4><FontAwesomeIcon icon="tools" /> 修复工具</h4>
            </div>
            <div class="tools-grid">
              <button v-for="tool in tools" :key="tool.id"
                      class="tool-btn" :class="{active: activeTool === tool.id}"
                      @click="selectTool(tool.id)">
                <FontAwesomeIcon :icon="tool.icon" />
                <span>{{ tool.name }}</span>
              </button>
            </div>

            <div class="piece-palette">
              <h5><FontAwesomeIcon icon="shapes" /> 碎片面板</h5>
              <div class="pieces-grid">
                <div v-for="piece in availablePieces" :key="piece.id"
                     class="palette-piece" draggable="true"
                     @dragstart="onDragStart(piece.id)"
                     :style="{
                       backgroundImage: `url(${selectedArtifact?.puzzleImage})`,
                       backgroundPosition: piece.bgPosition
                     }">
                  <div class="piece-label">{{ piece.id }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="workbench-footer">
          <div class="timer">
            <FontAwesomeIcon icon="clock" />
            <span>{{ formatTime(elapsedTime) }}</span>
          </div>
          <div class="piece-count">
            <FontAwesomeIcon icon="puzzle-piece" />
            <span>{{ availablePieces.length }} 个剩余碎片</span>
          </div>
          <button class="btn btn-primary" @click="checkCompletion"
                  :disabled="placedPiecesCount < totalPiecesCount">
            <FontAwesomeIcon icon="check" />
            <span>完成修复</span>
          </button>
        </div>
      </div>

      <!-- 右侧信息面板 -->
      <div class="info-panel">
        <div class="panel-section artifact-history">
          <h4><FontAwesomeIcon icon="history" /> 文物历史</h4>
          <div class="history-content" v-if="selectedArtifact">
            <p>{{ selectedArtifact.history }}</p>
            <div class="damage-info">
              <h5>损伤情况</h5>
              <ul>
                <li v-for="damage in selectedArtifact.damages" :key="damage.type">
                  <FontAwesomeIcon icon="exclamation-triangle" />
                  <span>{{ damage.type }}：{{ damage.description }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="panel-section repair-guide">
          <h4><FontAwesomeIcon icon="book" /> 修复指南</h4>
          <div class="guide-steps">
            <div v-for="step in guideSteps" :key="step.id"
                 class="guide-step" :class="{current: currentStep === step.id}">
              <div class="step-number">{{ step.id }}</div>
              <div class="step-content">
                <h5>{{ step.title }}</h5>
                <p>{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="panel-section repair-records">
          <h4><FontAwesomeIcon icon="chart-bar" /> 修复记录</h4>
          <div class="records-list">
            <div v-for="record in repairRecords" :key="record.id"
                 class="record-item">
              <div class="record-header">
                <span class="artifact-name">{{ record.artifact }}</span>
                <span class="record-date">{{ record.date }}</span>
              </div>
              <div class="record-stats">
                <span>用时：{{ record.time }}</span>
                <span>准确率：{{ record.accuracy }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 完成修复模态框 -->
    <div class="modal-overlay" v-if="showCompletionModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>修复完成！</h2>
          <button class="close-btn" @click="closeCompletionModal">
            <FontAwesomeIcon icon="times" />
          </button>
        </div>
        <div class="modal-body">
          <div class="completion-stats">
            <div class="stat-card">
              <div class="stat-icon">
                <FontAwesomeIcon icon="clock" />
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ formatTime(elapsedTime) }}</div>
                <div class="stat-label">修复用时</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">
                <FontAwesomeIcon icon="check-circle" />
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ accuracy }}%</div>
                <div class="stat-label">修复准确率</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">
                <FontAwesomeIcon icon="star" />
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ earnedScore }}</div>
                <div class="stat-label">获得积分</div>
              </div>
            </div>
          </div>

          <div class="achievement-unlocked" v-if="newAchievement">
            <div class="achievement-badge">
              <FontAwesomeIcon :icon="newAchievement.icon" />
            </div>
            <div class="achievement-text">
              <h4>解锁新成就！</h4>
              <p>{{ newAchievement.name }}</p>
            </div>
          </div>

          <div class="artifact-restored">
            <div class="restored-image"></div>
            <div class="restored-info">
              <h3>{{ selectedArtifact?.name }}</h3>
              <p>已成功修复并加入您的收藏</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="closeCompletionModal">
            继续修复
          </button>
          <button class="btn btn-primary" @click="shareResult">
            <FontAwesomeIcon icon="share" />
            <span>分享成果</span>
          </button>
          <button class="btn btn-primary" @click="nextArtifact">
            <FontAwesomeIcon icon="arrow-right" />
            <span>下一件文物</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

// 状态管理
const selectedDifficulty = ref('all')
const selectedArtifact = ref(null)
const showGrid = ref(true)
const magnetismEnabled = ref(true)
const referenceVisible = ref(true)
const referenceOpacity = ref(0.3)
const activeTool = ref('move')
const elapsedTime = ref(0)
const showCompletionModal = ref(false)
const accuracy = ref(95)
const earnedScore = ref(250)
const newAchievement = ref(null)

// 用户数据
const userStats = reactive({
  completed: 8,
  score: 1850,
  rank: 15
})

// 文物数据
const artifacts = ref([
  {
    id: 1,
    name: '青铜鼎',
    era: '商代',
    material: '青铜',
    difficulty: 'medium',
    status: 'in_progress',
    pieceCount: 36,
    avgTime: 45,
    image: '/images/bronze_ding.jpg',
    referenceImage: '/images/bronze_ding_ref.jpg',
    puzzleImage: '/images/bronze_ding_puzzle.jpg',
    history: '这件青铜鼎出土于河南安阳殷墟，是商代晚期的重要礼器...',
    damages: [
      { type: '断裂', description: '器身有三处断裂' },
      { type: '锈蚀', description: '表面有严重锈蚀' },
      { type: '缺失', description: '部分纹饰缺失' }
    ]
  },
  // 更多文物...
])

const achievements = ref([
  { id: 1, name: '新手修复师', description: '完成第一个文物修复', icon: 'star', unlocked: true, progress: 100 },
  { id: 2, name: '青铜专家', description: '修复3件青铜器', icon: 'dragon', unlocked: false, progress: 66 },
  { id: 3, name: '速度之星', description: '在30分钟内完成修复', icon: 'bolt', unlocked: false, progress: 45 },
  { id: 4, name: '完美主义', description: '准确率达到95%以上', icon: 'check-double', unlocked: true, progress: 100 }
])

// 拼图数据
const puzzlePieces = ref([])
const dropZones = ref([])
const pieceSize = 60
const gridSize = 8

// 计算属性
const filteredArtifacts = computed(() => {
  if (selectedDifficulty.value === 'all') {
    return artifacts.value
  }
  return artifacts.value.filter(a => a.difficulty === selectedDifficulty.value)
})

const availablePieces = computed(() => {
  return puzzlePieces.value.filter(p => !p.placed)
})

const placedPiecesCount = computed(() => {
  return puzzlePieces.value.filter(p => p.placed).length
})

const totalPiecesCount = computed(() => {
  return puzzlePieces.value.length
})

// 修复工具
const tools = ref([
  { id: 'move', name: '移动', icon: 'arrows' },
  { id: 'rotate', name: '旋转', icon: 'rotate-right' },
  { id: 'zoom', name: '缩放', icon: 'search' },
  { id: 'eraser', name: '橡皮', icon: 'eraser' },
  { id: 'paint', name: '上色', icon: 'paint-brush' },
  { id: 'measure', name: '测量', icon: 'ruler' }
])

// 修复指南步骤
const guideSteps = ref([
  { id: 1, title: '清理碎片', description: '将碎片按形状和颜色分类' },
  { id: 2, title: '拼接轮廓', description: '先拼接文物的外轮廓' },
  { id: 3, title: '填充内部', description: '逐步填充内部碎片' },
  { id: 4, title: '检查细节', description: '检查纹饰和图案是否匹配' },
  { id: 5, title: '最终调整', description: '微调位置，完成修复' }
])

const currentStep = ref(1)

const repairRecords = ref([
  { id: 1, artifact: '唐代彩陶罐', date: '2024-03-15', time: '38分钟', accuracy: 92 },
  { id: 2, artifact: '宋代玉佩', date: '2024-03-10', time: '52分钟', accuracy: 88 },
  { id: 3, artifact: '汉代铜镜', date: '2024-03-05', time: '41分钟', accuracy: 95 }
])

// 方法
const filterArtifacts = () => {
  // 筛选文物
}

const selectArtifact = (artifact) => {
  selectedArtifact.value = artifact
  initializePuzzle(artifact)
}

const initializePuzzle = (artifact) => {
  // 初始化拼图
  puzzlePieces.value = []
  dropZones.value = []

  const pieces = []
  const zones = []

  for (let i = 0; i < artifact.pieceCount; i++) {
    const row = Math.floor(i / 6)
    const col = i % 6

    pieces.push({
      id: i + 1,
      x: Math.random() * 500,
      y: Math.random() * 300,
      bgPosition: `${-col * pieceSize}px ${-row * pieceSize}px`,
      placed: false,
      hint: false
    })

    zones.push({
      id: i + 1,
      x: 200 + col * pieceSize,
      y: 100 + row * pieceSize
    })
  }

  puzzlePieces.value = pieces
  dropZones.value = zones
  elapsedTime.value = 0
}

const onDragStart = (pieceId) => {
  // 开始拖拽
}

const onTouchStart = (pieceId, event) => {
  // 触摸开始
}

const onDrop = (event) => {
  // 放置碎片
}

const showHint = () => {
  // 显示提示
}

const resetPuzzle = () => {
  if (selectedArtifact.value) {
    initializePuzzle(selectedArtifact.value)
  }
}

const toggleGrid = () => {
  showGrid.value = !showGrid.value
}

const toggleMagnetism = () => {
  magnetismEnabled.value = !magnetismEnabled.value
}

const toggleReference = () => {
  referenceVisible.value = !referenceVisible.value
}

const adjustReferenceOpacity = (delta) => {
  referenceOpacity.value = Math.max(0, Math.min(1, referenceOpacity.value + delta))
}

const selectTool = (toolId) => {
  activeTool.value = toolId
}

const checkCompletion = () => {
  if (placedPiecesCount.value === totalPiecesCount.value) {
    showCompletionModal.value = true
    // 计算分数和准确率
  }
}

const closeCompletionModal = () => {
  showCompletionModal.value = false
}

const shareResult = () => {
  // 分享修复结果
}

const nextArtifact = () => {
  // 下一件文物
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

// 计时器
let timer
onMounted(() => {
  timer = setInterval(() => {
    elapsedTime.value++
  }, 1000)

  // 初始化第一个文物
  if (artifacts.value.length > 0) {
    selectArtifact(artifacts.value[0])
  }
})
</script>

<style scoped>
.repair-lab-view {
  height: 100vh;
  background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
  display: flex;
  flex-direction: column;
}

.lab-header {
  background: var(--surface);
  padding: 20px 32px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.subtitle {
  color: var(--text-secondary);
  font-size: 16px;
}

.user-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.lab-container {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr 320px;
  overflow: hidden;
}

.artifact-selection {
  background: var(--surface);
  border-right: 1px solid var(--border-color);
  overflow-y: auto;
  padding: 24px;
}

.selection-header {
  margin-bottom: 24px;
}

.selection-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.difficulty-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.difficulty-label {
  font-size: 14px;
  color: var(--text-secondary);
}

select {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--surface);
  color: var(--text-primary);
  font-size: 14px;
}

.artifact-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.artifact-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.artifact-card.selected {
  border-color: var(--primary);
  transform: translateX(4px);
}

.artifact-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.artifact-image {
  height: 120px;
  position: relative;
  background-size: cover;
  background-position: center;
}

.artifact-status {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.artifact-status.in_progress {
  background: #fef3c7;
  color: #d97706;
}

.artifact-status.completed {
  background: #d1fae5;
  color: #059669;
}

.artifact-difficulty {
  position: absolute;
  bottom: 8px;
  left: 8px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
}

.artifact-difficulty.easy {
  background: #10b981;
}

.artifact-difficulty.medium {
  background: #f59e0b;
}

.artifact-difficulty.hard {
  background: #ef4444;
}

.artifact-info {
  padding: 12px;
}

.artifact-info h4 {
  font-size: 16px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.artifact-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.artifact-meta .era,
.artifact-meta .material {
  font-size: 12px;
  padding: 2px 8px;
  background: var(--surface-hover);
  border-radius: 10px;
  color: var(--text-secondary);
}

.artifact-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
}

.artifact-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-achievements h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.achievements-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.achievement-item.unlocked {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
}

.achievement-icon {
  width: 40px;
  height: 40px;
  background: var(--primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
}

.achievement-info {
  flex: 1;
}

.achievement-info h5 {
  font-size: 14px;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.achievement-info p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.achievement-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: var(--surface-hover);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s;
}

.achievement-progress span {
  font-size: 12px;
  color: var(--text-secondary);
  min-width: 40px;
}

.repair-workbench {
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  overflow: hidden;
}

.workbench-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: var(--surface);
  border-bottom: 1px solid var(--border-color);
}

.artifact-info h3 {
  font-size: 20px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.artifact-details {
  display: flex;
  gap: 12px;
}

.artifact-details span {
  font-size: 14px;
  padding: 4px 12px;
  background: var(--surface-hover);
  border-radius: 12px;
  color: var(--text-secondary);
}

.artifact-details .difficulty {
  color: white;
}

.artifact-details .difficulty.medium {
  background: #f59e0b;
}

.workbench-controls {
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
  font-size: 14px;
}

.control-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.workbench-container {
  flex: 1;
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  gap: 24px;
  padding: 24px;
  overflow: hidden;
}

.reference-view {
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.reference-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--surface-hover);
}

.reference-header h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin: 0;
  color: var(--text-primary);
}

.reference-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ref-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: var(--surface);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 12px;
}

.opacity-display {
  font-size: 12px;
  color: var(--text-secondary);
  min-width: 40px;
  text-align: center;
}

.reference-image {
  flex: 1;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}

.puzzle-area {
  position: relative;
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.puzzle-area.grid {
  background-image:
    linear-gradient(var(--border-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
  background-size: 20px 20px;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20px, 1fr));
  grid-template-rows: repeat(auto-fill, minmax(20px, 1fr));
  pointer-events: none;
}

.grid-line {
  border-right: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
}

.puzzle-piece {
  position: absolute;
  background-color: white;
  background-size: 600% 600%;
  border: 1px solid var(--border-color);
  cursor: move;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--text-secondary);
  transition: all 0.3s;
}

.puzzle-piece.placed {
  opacity: 0.8;
  cursor: default;
}

.puzzle-piece:hover:not(.placed) {
  transform: scale(1.05);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.piece-id {
  position: absolute;
  top: 4px;
  left: 4px;
  background: rgba(255, 255, 255, 0.8);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.piece-hint {
  position: absolute;
  bottom: 4px;
  right: 4px;
  color: #f59e0b;
  animation: pulse 2s infinite;
}

.drop-zones {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.drop-zone {
  position: absolute;
  border: 2px dashed var(--primary);
  opacity: 0.3;
  pointer-events: none;
}

.puzzle-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px;
  border-top: 1px solid var(--border-color);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--text-primary);
}

.progress-bar {
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

.tool-panel {
  background: var(--surface);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.tools-header {
  padding: 12px 16px;
  background: var(--surface-hover);
  border-bottom: 1px solid var(--border-color);
}

.tools-header h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin: 0;
  color: var(--text-primary);
}

.tools-grid {
  padding: 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.tool-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  background: var(--surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
}

.tool-btn:hover {
  background: var(--surface-hover);
  color: var(--text-primary);
}

.tool-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.tool-btn svg {
  font-size: 20px;
}

.tool-btn span {
  font-size: 12px;
}

.piece-palette {
  flex: 1;
  padding: 16px;
  border-top: 1px solid var(--border-color);
}

.piece-palette h5 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.pieces-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.palette-piece {
  aspect-ratio: 1;
  background-color: white;
  background-size: 300% 300%;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  cursor: move;
  position: relative;
}

.piece-label {
  position: absolute;
  top: 2px;
  left: 2px;
  background: rgba(255, 255, 255, 0.8);
  width: 16px;
  height: 16px;
  border-radius: 50%;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.workbench-footer {
  padding: 16px 24px;
  background: var(--surface);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timer, .piece-count {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  color: var(--text-primary);
}

.info-panel {
  background: var(--surface);
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
  padding: 24px;
}

.panel-section {
  margin-bottom: 32px;
}

.panel-section h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.history-content p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.damage-info h5 {
  font-size: 14px;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.damage-info ul {
  list-style: none;
  padding: 0;
}

.damage-info li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--text-secondary);
}

.damage-info li svg {
  color: #ef4444;
  margin-top: 2px;
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.guide-step {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 12px;
  transition: all 0.3s;
}

.guide-step.current {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border: 1px solid var(--primary);
}

.step-number {
  width: 28px;
  height: 28px;
  background: var(--primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h5 {
  font-size: 14px;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.step-content p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  background: var(--bg-secondary);
  padding: 12px;
  border-radius: 8px;
}

.record-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.artifact-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.record-date {
  font-size: 12px;
  color: var(--text-secondary);
}

.record-stats {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary);
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px 32px 16px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  font-size: 28px;
  color: var(--text-primary);
  margin: 0;
}

.modal-body {
  padding: 32px;
}

.completion-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.stat-info .stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.stat-info .stat-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.achievement-unlocked {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 193, 7, 0.1));
  border-radius: 12px;
  margin-bottom: 32px;
}

.achievement-badge {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #ffd700, #ffc107);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.achievement-text h4 {
  font-size: 20px;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.achievement-text p {
  color: var(--text-secondary);
}

.artifact-restored {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 12px;
}

.restored-image {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  border-radius: 12px;
}

.restored-info h3 {
  font-size: 24px;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.restored-info p {
  color: var(--text-secondary);
}

.modal-footer {
  padding: 16px 32px 32px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@media (max-width: 1400px) {
  .lab-container {
    grid-template-columns: 1fr;
  }

  .artifact-selection,
  .info-panel {
    display: none;
  }
}
</style>