export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated, isAdmin, user } = useAuthStore()
  
  // Public routes are always accessible
  const publicRoutes = ['/login', '/', '/register']
  if (publicRoutes.includes(to.path)) {
    return
  }

  // Require authentication for all other routes
  if (!isAuthenticated) {
    return navigateTo('/login')
  }

  // Require active account
  if (!user?.is_active) {
    return navigateTo('/account-inactive')
  }

  // Admin routes need superuser status
  if (to.path.startsWith('/admin') && !isAdmin) {
    return navigateTo('/')
  }

  // Subscription required routes
  if (to.path.startsWith('/translate')) {
    const subscription = user?.subscription
    if (!subscription?.is_active) {
      return navigateTo('/subscription')
    }
  }
})
