export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated } = useAuthStore()
  
  // If user is already authenticated, redirect to profile
  if (isAuthenticated) {
    return navigateTo('/profile')
  }
})
