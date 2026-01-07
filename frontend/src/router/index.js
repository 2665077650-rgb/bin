import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: '时空博物馆 - 首页'
    }
  },
  {
    path: '/virtual-tour',
    name: 'VirtualTour',
    component: () => import('@/views/VirtualTourView.vue'),
    meta: {
      title: '3D虚拟展厅 - 时空博物馆'
    }
  },
  {
    path: '/time-map',
    name: 'TimeMap',
    component: () => import('@/views/TimeMapView.vue'),
    meta: {
      title: '时空地图 - 时空博物馆'
    }
  },
  {
    path: '/repair-lab',
    name: 'RepairLab',
    component: () => import('@/views/RepairLabView.vue'),
    meta: {
      title: '虚拟修复实验室 - 时空博物馆'
    }
  },
  {
    path: '/artifact/:id',
    name: 'ArtifactDetail',
    component: () => import('@/views/ArtifactDetailView.vue'),
    meta: {
      title: '文物详情 - 时空博物馆'
    }
  },
  {
    path: '/exhibition/:id',
    name: 'ExhibitionDetail',
    component: () => import('@/views/ExhibitionDetailView.vue'),
    meta: {
      title: '展览详情 - 时空博物馆'
    }
  },
  {
    path: '/ai-guide',
    name: 'AIGuide',
    component: () => import('@/views/AIGuideView.vue'),
    meta: {
      title: 'AI智能解说 - 时空博物馆'
    }
  },
  {
    path: '/user/collection',
    name: 'UserCollection',
    component: () => import('@/views/UserCollectionView.vue'),
    meta: {
      title: '我的收藏 - 时空博物馆'
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/SearchView.vue'),
    meta: {
      title: '搜索 - 时空博物馆'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: '页面未找到 - 时空博物馆'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫：更新页面标题
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '时空博物馆'
  next()
})

// 路由守卫：页面切换动画
router.afterEach((to, from) => {
  // 可以在这里添加页面切换动画
})

export default router