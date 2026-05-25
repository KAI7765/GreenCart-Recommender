import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },

  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: () => import('../views/RecommendationsView.vue')
  },
  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetailView.vue')
  },
  {
    path: '/collection',
    name: 'Collection',
    component: () => import('../views/CollectionView.vue')
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/CartView.vue')
  },
  {
    path: '/preferences',
    name: 'Preferences',
    component: () => import('../views/PreferencesView.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/AdminView.vue'),
    children: [
      {
        path: 'labels',
        name: 'AdminLabels',
        component: () => import('../components/admin/LabelManagement.vue')
      },
      {
        path: 'products',
        name: 'AdminProducts',
        component: () => import('../components/admin/ProductManagement.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../components/admin/UserAnalysis.vue')
      },
      {
        path: 'analytics',
        name: 'AdminAnalytics',
        component: () => import('../components/admin/Analytics.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router