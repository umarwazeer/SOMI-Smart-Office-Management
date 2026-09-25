import AuthenticationService from "src/pages/authentication/AuthenticationService";

// boot/router-auth-guard.js

export default async ({ router }) => {
  router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    const token = AuthenticationService.getToken();

    if (requiresAuth && !token) {
      next('LoginPage'); // Redirect to login page
    } else {
      next();
    }
  });
};
