<script setup lang="ts">
const router = useRouter()
const authStore = useAuthStore()

// SEO metadata
useSeoMeta({
  title: 'Subtly - AI-Powered Video Subtitle Translation',
  description: 'Transform your video content with AI-powered subtitle translation. Upload your videos and get accurate translations in multiple languages.',
  ogTitle: 'Subtly - AI-Powered Video Subtitle Translation',
  ogDescription: 'Get accurate subtitle translations in multiple languages using state-of-the-art AI technology.',
  ogImage: '/og-image.jpg',  // Make sure to add this image
  twitterCard: 'summary_large_image',
})

const features = [
  {
    title: 'AI-Powered Translation',
    description: 'State-of-the-art machine learning models ensure accurate and natural-sounding translations.',
    icon: 'i-heroicons-cpu-chip'
  },
  {
    title: 'Multiple Languages',
    description: 'Support for a wide range of languages to reach your global audience.',
    icon: 'i-heroicons-language'
  },
  {
    title: 'Easy Integration',
    description: 'Simple workflow to upload, translate, and download your subtitled videos.',
    icon: 'i-heroicons-arrow-path-rounded-square'
  }
]
</script>

<template>
  <UContainer>
    <div class="flex flex-col items-center justify-center space-y-8 py-12">
      <h1 class="text-4xl font-bold">
        Welcome to Subtly
      </h1>
      
      <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl text-center">
        Transform your video content with AI-powered subtitle translation. 
        Upload your videos and get accurate translations in multiple languages.
      </p>

      <div class="flex gap-4">
        <UButton
          v-if="!authStore.isAuthenticated"
          to="/login"
          size="xl"
          icon="i-heroicons-arrow-right"
        >
          Get Started
        </UButton>
        <UButton
          v-else
          to="/translate"
          size="xl"
          icon="i-heroicons-language"
        >
          Start Translating
        </UButton>
      </div>

      <!-- Features Section -->
      <div class="grid md:grid-cols-3 gap-8 mt-16">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="p-6 rounded-xl border border-gray-200 dark:border-gray-800"
        >
          <UIcon
            :name="feature.icon"
            class="w-12 h-12 mb-4 text-primary-500"
          />
          <h3 class="text-xl font-semibold mb-2">
            {{ feature.title }}
          </h3>
          <p class="text-gray-600 dark:text-gray-400">
            {{ feature.description }}
          </p>
        </div>
      </div>
    </div>
  </UContainer>
</template>
