const routes = [
  {
    path: '/',
    component: () => import('src/layouts/EMSLayout.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        redirect: 'emp-dashboard'
      },

      {
        path: 'api-test',
        component: () => import('src/pages/ApiTest.vue')
      },

      {
        path: 'emp-dashboard',
        component: () => import('src/pages/component/dashboard/emp-dashboard.vue')
      },

      {
        path: 'Empl-list',
        component: () => import('src/pages/component/empl-list.vue')
      },

      {
        path: 'LeaveReport',
        component: () => import('src/pages/component/EmployeeReports/LeaveReport.vue')
      },

      {
        path: 'tabs',
        component: () => import('src/pages/component/tabs.vue')
      },

      {
        path: 'leavePage',
        component: () => import('src/pages/component/Leave/leavePage.vue')
      },

      {
        path: 'LeaveDetailsDialog',
        component: () => import('src/pages/component/Leave/LeaveDetailsDialog.vue')
      },

      {
        path: 'mytabs',
        component: () => import('src/pages/component/mytabs.vue')
      },

      {
        path: 'attan_report',
        component: () => import('src/pages/component/attandence/attan_report.vue')
      },

      {
        path: 'camera',
        component: () => import('src/pages/component/attandence/camera.vue')
      },

      {
        path: 'list_dep',
        component: () => import('src/pages/component/department/list_dep.vue')
      },

      {
        path: 'addDep',
        component: () => import('src/pages/component/department/addDep.vue')
      },

      {
        path: 'users',
        component: () => import('src/pages/component/users.vue')
      },

      {
        path: 'test',
        component: () => import('src/pages/component/test.vue')
      },

      {
        path: 'LSelect',
        component: () => import('src/pages/component/LSelect.vue')
      },

      {
        path: 'imageUploader',
        component: () => import('src/pages/component/imageUploader.vue')
      },

      {
        path: 'Approver_leaves',
        component: () => import('src/pages/component/Leave/Approver_leaves.vue')
      },

      {
        path: 'add_employee',
        component: () => import('src/pages/component/employee/add_employee.vue')
      },

      {
        path: 'payroll_report',
        component: () => import('src/pages/component/payroll/payroll_report.vue')
      },

      {
        path: 'new_payroll',
        component: () => import('src/pages/component/payroll/new_payroll.vue')
      },

      {
        path: 'edit_payroll',
        component: () => import('src/pages/component/payroll/edit_payroll.vue')
      },

      {
        path: 'tasks',
        component: () => import('src/pages/component/tasks/TasksPage.vue')
      },

      {
        path: 'performance',
        component: () => import('src/pages/component/performance/PerformancePage.vue')
      },

      {
        path: 'intelligence',
        component: () => import('src/pages/component/intelligence/IntelligenceDashboard.vue')
      },

      {
        path: 'ai-assistant',
        component: () => import('src/pages/component/intelligence/AIAssistant.vue')
      },

      {
        path: 'EmployeeDetails/:id',
        component: () => import('src/pages/component/EmployeeReports/EmployeeDetails.vue')
      },

      {
        path: 'AccountSettings',
        component: () => import('src/pages/component/AccountSettings.vue')
      },

      // Keep the catch-all child route LAST.
      {
        path: ':catchAll(.*)*',
        component: () => import('src/pages/errors/ErrorNotFound.vue')
      }
    ]
  },

  {
    path: '/',
    component: () => import('src/layouts/blanck.vue'),
    children: [
      {
        path: 'SignUp',
        component: () => import('src/pages/authentication/SignUp.vue')
      },

      {
        path: 'LoginPage',
        component: () => import('src/pages/authentication/LoginPage.vue')
      }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/errors/ErrorNotFound.vue')
  }
]

export default routes
