<script setup lang="ts">
// https://nuxt.com/docs/guide/directory-structure/pages
definePageMeta({
  middleware: 'guest'
})

const route = useRoute()
const authStore = useAuthStore()
const toast = useToast()

interface OAuthResponse {
  access_token?: string
  error?: string
}

// Handle OAuth callback
const { data, pending } = await useFetch<OAuthResponse>('/api/auth/verify-oauth-token', {
  method: 'POST',
  body: {
    token: route.query.code
  }
})

// Watch for data changes
watchEffect(() => {
  if (data.value?.error) {
    toast.add({
      title: 'Authentication Error',
      description: data.value.error,
      color: 'error'
    })
    navigateTo('/login')
    return
  }

  if (data.value?.access_token) {
    // Update auth cookie with the verified token
    const tokenCookie = useCookie('access_token', {
      maxAge: 60 * 60 * 24, // 1 day
      path: '/',
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production'
    })
    tokenCookie.value = data.value.access_token
    
    // Fetch user data and redirect
    authStore.fetchUser()
    navigateTo('/profile')
  }
})
</script>

<template>
  <div class="flex min-h-screen items-center justify-center">
    <template v-if="pending">
      <UCard>
        <div class="flex flex-col items-center gap-4 p-4">
          <UIcon name="i-heroicons-arrow-path" class="animate-spin h-8 w-8" />
          <p>Verifying your login...</p>
        </div>
      </UCard>
    </template>
  </div>
</template>
