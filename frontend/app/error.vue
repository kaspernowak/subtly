<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

// Error is handled by Nuxt
const error = useError()

// Add SEO metadata
useSeoMeta({
  title: `Error ${error.value?.statusCode || ''}`,
  description: error.value?.message || 'An error occurred',
  robots: 'noindex, nofollow'
})

function handleError() {
  clearError()
  navigateTo('/')
}
</script>

<template>
  <UContainer>
    <div class="min-h-[400px] flex flex-col items-center justify-center text-center">
      <div v-if="error?.statusCode === 404">
        <h1 class="text-4xl font-bold mb-4">Page Not Found</h1>
        <p class="text-gray-600 dark:text-gray-400 mb-8">
          The page you are looking for doesn't exist or has been moved.
        </p>
      </div>
      <div v-else>
        <h1 class="text-4xl font-bold mb-4">Something went wrong</h1>
        <p class="text-gray-600 dark:text-gray-400 mb-8">
          {{ error?.message || 'An error occurred while processing your request.' }}
        </p>
      </div>
      
      <UButton
        icon="i-heroicons-arrow-left"
        @click="handleError"
      >
        Back to Home
      </UButton>
    </div>
  </UContainer>
</template>
