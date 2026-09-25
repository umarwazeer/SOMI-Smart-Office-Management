
const routes = [
  {
    path: '/',
    component: () => import('src/layouts/EMSLayout.vue'),
    meta: {requiresAuth: true},
    children: [
      // { path: 'HomePage', component: () => import('src/pages/HomePage.vue') },
      { path: '*', component: () => import('../pages/errors/ErrorNotFound.vue') },
      { path: 'attan_report',  component: () => import('src/pages/component/attandence/attan_report') },
      { path: 'emp-dashboard', component: () => import('src/pages/component/dashboard/emp-dashboard.vue') },
      { path: 'Empl-list', component: () => import('src/pages/component/empl-list.vue') },
      { path: 'tabs', component: () => import('src/pages/component/tabs.vue') },
      { path: 'leavePage', component: () => import('src/pages/component/Leave/leavePage.vue') },
      { path: 'LeaveDetailsDialog', component: () => import('src/pages/component/Leave/LeaveDetailsDialog.vue') },
      { path: 'mytabs', component: () => import('src/pages/component/mytabs.vue') },
      // { path: 'LoginPage', component: () => import('src/pages/LoginPage.vue') },
      { path: 'new_attandence', component: () => import('src/pages/component/attandence/new_attandence') },
      { path: 'list_dep', component: () => import('src/pages/component/department/list_dep') },
      { path: 'addDep', component: () => import('src/pages/component/department/addDep') },
      { path: 'addDep', component: () => import('src/pages/component/department/addDep') },
      { path: 'users', component: () => import('src/pages/component/users') },
      { path: 'test', component: () => import('src/pages/component/test.vue') },
      { path: 'LSelect', component: () => import('src/pages/component/LSelect.vue') },
      { path: 'imageUploader', component: () => import('src/pages/component/imageUploader.vue') },
      { path: 'Approver_leaves', component: () => import('src/pages/component/Leave/Approver_leaves.vue') },
      { path: 'camera', component: () => import('src/pages/component/attandence/camera.vue')},
      { path: 'add_employee', component: () => import('src/pages/component/employee/add_employee.vue')},
      { path: 'attandenceForm', component: () => import('src/pages/component/attandence/attandenceForm.vue')},
      { path: 'payroll_report', component: () => import('src/pages/component/payroll/payroll_report.vue') },
      { path: 'new_payroll', component: () => import('src/pages/component/payroll/new_payroll.vue') },
      { path: 'edit_payroll', component: () => import('src/pages/component/payroll/edit_payroll.vue') },
      { path: 'EmployeeDetails', component: () => import('src/pages/component/EmployeeReports/EmployeeDetails.vue') },
      { path: 'AccountSettings', component: () => import('src/pages/component/AccountSettings.vue') },
      // { path: 'SignUp', component: () => import('src/pages/authentication/SignUp.vue') },




    ]
  },
  {
    path: '/',
    component: () => import('src/layouts/blanck.vue'),
    children: [
      { path: 'SignUp', component: () => import('src/pages/authentication/SignUp.vue') },
      { path: 'LoginPage', component: () => import('src/pages/authentication/LoginPage.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/errors/ErrorNotFound.vue')
  }
]

export default routes
