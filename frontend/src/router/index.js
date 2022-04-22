import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },

  {
    path: '/resource',
    component: Layout,
    children: [{
      path: 'index',
      name: '资产',
      component: () => import('@/views/resource/index'),
      meta: { title: '资产', icon: 'list' }
    }]
  },

  {
    path: '/service',
    component: Layout,
    children: [{
      path: 'index',
      name: '服务',
      component: () => import('@/views/service/index'),
      meta: { title: '服务', fontawesomeicon: 'fa-cubes' }
    }]
  },

  {
    path: '/task',
    component: Layout,
    children: [{
      path: 'index',
      name: '任务管理',
      component: () => import('@/views/task/index'),
      meta: { title: '任务管理', fontawesomeicon: 'fa-server' }
    }]
  },

  {
    path: '/vul',
    component: Layout,
    children: [{
      path: 'index',
      name: '漏洞报告',
      component: () => import('@/views/vul/index'),
      meta: { title: '漏洞报告', fontawesomeicon: 'fa-bug' }
    }]
  },

  {
    path: '/schedule',
    component: Layout,
    children: [{
      path: 'index',
      name: '定时任务',
      component: () => import('@/views/schedule/index'),
      meta: { title: '定时任务', fontawesomeicon: 'fa-clock' }
    }]
  },
  {
    path: '/config',
    component: Layout,
    children: [{
      path: 'index',
      name: '配置',
      component: () => import('@/views/config/index'),
      meta: { title: '配置', fontawesomeicon: 'fa-gear' }
    }]
  },
  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://site.ccreater.top/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
