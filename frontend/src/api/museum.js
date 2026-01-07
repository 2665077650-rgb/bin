import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 添加认证token
    const token = localStorage.getItem('museum_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // 处理未授权
      localStorage.removeItem('museum_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API接口定义
export const museumAPI = {
  // 文物相关
  getArtifacts: (params) => api.get('/artifacts', { params }),
  getArtifact: (id) => api.get(`/artifacts/${id}`),
  searchArtifacts: (query) => api.get('/artifacts/search', { params: { q: query } }),

  // 展览相关
  getExhibitions: () => api.get('/exhibitions'),
  getExhibition: (id) => api.get(`/exhibitions/${id}`),

  // 时间轴相关
  getTimeline: () => api.get('/timeline'),
  getEvents: (params) => api.get('/events', { params }),

  // 地图相关
  getMapMarkers: () => api.get('/map/markers'),
  getHeatmapData: () => api.get('/map/heatmap'),

  // 修复相关
  getRepairPuzzle: (artifact_id) => api.get(`/repair/puzzle/${artifact_id}`),
  submitRepair: (data) => api.post('/repair/complete', data),

  // AI相关
  getAIExplanation: (data) => api.post('/ai/explain', data),

  // 用户相关
  getUserProfile: () => api.get('/user/profile'),
  updateUserProfile: (data) => api.put('/user/profile', data),
  getUserCollection: () => api.get('/user/collection'),
  addToCollection: (artifact_id) => api.post('/user/collection', { artifact_id }),

  // 统计相关
  getStatistics: () => api.get('/statistics'),
  getUserStats: () => api.get('/user/stats'),

  // 文件上传
  uploadImage: (formData) => api.post('/upload/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 导出常用的API方法
export const fetchArtifacts = museumAPI.getArtifacts
export const fetchExhibitions = museumAPI.getExhibitions
export const fetchTreasure = museumAPI.getArtifact
export const submitRepairResult = museumAPI.submitRepair
export const getAIResponse = museumAPI.getAIExplanation

export default museumAPI