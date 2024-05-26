export default defineNuxtRouteMiddleware((to, from) => {
  const isLoggedIn = localStorage.getItem("access_token");
  if (!["/login", "/register"].includes(to.path) && !isLoggedIn) {
    return navigateTo("/login");
  }
  if (["/login", "/register"].includes(to.path)  && isLoggedIn) {
    return navigateTo("/");
  }
})

