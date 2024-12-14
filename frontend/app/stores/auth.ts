import { defineStore } from 'pinia'

interface User {
  id: string
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  subscription?: {
    plan: {
      name: 'free' | 'basic' | 'pro'
      character_limit: number
    }
    characters_used: number
    is_active: boolean
  }
}

interface LoginResponse {
  access_token: string
  token_type: string
}

export const useAuthStore = defineStore('auth', () => {
  // State with SSR-safe cookie
  const token = useCookie('access_token', {
    maxAge: 60 * 60 * 24, // 1 day
    path: '/',
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production'
  })
  
  const user = useState<User | null>('auth:user', () => null)
  const loading = useState<boolean>('auth:loading', () => false)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_superuser ?? false)
  const subscription = computed(() => user.value?.subscription)
  const remainingCharacters = computed(() => {
    if (!subscription.value) return 0
    return subscription.value.plan.character_limit - subscription.value.characters_used
  })

  // Actions
  async function login(email: string, password: string) {
    try {
      loading.value = true
      const formData = new FormData()
      formData.append('username', email)  // FastAPI OAuth expects 'username'
      formData.append('password', password)

      const response = await $fetch<LoginResponse>('/api/v1/login/access-token', {
        method: 'POST',
        body: formData
      })
      
      token.value = response.access_token
      await fetchUser()
      return true
    } catch (error) {
      console.error('Login error:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return null

    try {
      loading.value = true
      const headers: HeadersInit = {}
      
      // Add token only if we're on the client or if it's an SSR request
      if (process.client || (process.server && token.value)) {
        headers.Authorization = `Bearer ${token.value}`
      }

      user.value = await $fetch<User>('/api/v1/users/me', { headers })
    } catch (error) {
      console.error('Error fetching user:', error)
      logout()
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    navigateTo('/login')
  }

  // Initialize user data if token exists
  if (token.value) {
    fetchUser()
  }

  return {
    user,
    loading,
    isAuthenticated,
    isAdmin,
    subscription,
    remainingCharacters,
    login,
    logout,
    fetchUser
  }
})
