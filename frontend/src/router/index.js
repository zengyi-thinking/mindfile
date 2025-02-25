import { createRouter, createWebHistory } from 'vue-router';

// 导入视图组件
const LoginView = () => import('../views/LoginView.vue');
const RegisterView = () => import('../views/RegisterView.vue');
const DashboardView = () => import('../views/DashboardView.vue');
const MindMapView = () => import('../views/MindMapView.vue');
const MaterialsView = () => import('../views/MaterialsView.vue');
const UserSettingsView = () => import('../views/UserSettingsView.vue');

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/mindmaps',
    name: 'MindMaps',
    component: MindMapView,
    meta: { requiresAuth: true }
  },
  {
    path: '/materials',
    name: 'Materials',
    component: MaterialsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: UserSettingsView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token');
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router; 