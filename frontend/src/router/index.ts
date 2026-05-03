import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
    { path: '/articles', name: 'articles', component: () => import('@/views/ArticleListView.vue') },
    { path: '/articles/:slug', name: 'article-detail', component: () => import('@/views/ArticleDetailView.vue') },
    { path: '/tags', name: 'tags', component: () => import('@/views/TagView.vue') },
    { path: '/tags/:slug', name: 'tag-articles', component: () => import('@/views/ArticleListView.vue') },
    { path: '/search', name: 'search', component: () => import('@/views/SearchView.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    {
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', name: 'admin-dashboard', component: () => import('@/views/admin/AdminDashboardView.vue') },
        { path: 'articles', name: 'admin-articles', component: () => import('@/views/admin/AdminArticlesView.vue') },
        { path: 'articles/new', name: 'admin-article-new', component: () => import('@/views/admin/AdminArticleEditView.vue') },
        { path: 'articles/:id/edit', name: 'admin-article-edit', component: () => import('@/views/admin/AdminArticleEditView.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/views/NotFoundView.vue') },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'home' }
  }
})

export default router
