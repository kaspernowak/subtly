<script setup lang="ts">
import { z } from 'zod'
import type { FormSubmitEvent } from '#ui/types'

const router = useRouter()
const authStore = useAuthStore()

const schema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required')
})

type Schema = z.output<typeof schema>

const state = reactive<Schema>({
  email: '',
  password: ''
})

const error = ref('')
const isLoading = ref(false)

async function onSubmit(event: FormSubmitEvent<Schema>) {
  isLoading.value = true
  error.value = ''
  
  try {
    const success = await authStore.login(event.data.email, event.data.password)
    if (success) {
      router.push('/profile')
    } else {
      error.value = 'Invalid email or password'
    }
  } catch (e) {
    error.value = 'An error occurred during login'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <UContainer>
    <div class="flex items-center justify-center min-h-[calc(100vh-200px)]">
      <UCard class="w-full max-w-md">
        <template #header>
          <div class="text-center mb-8">
            <h1 class="text-3xl font-bold mb-2">Welcome to Subtly</h1>
            <p class="text-gray-600 dark:text-gray-400">Sign in to start translating subtitles</p>
          </div>
        </template>

        <UForm 
          :schema="schema"
          :state="state" 
          class="space-y-6" 
          @submit="onSubmit"
        >
          <UFormField 
            label="Email" 
            name="email"
          >
            <UInput
              v-model="state.email"
              type="email"
              placeholder="Enter your email"
              autocomplete="email"
            />
          </UFormField>

          <UFormField 
            label="Password" 
            name="password"
          >
            <UInput
              v-model="state.password"
              type="password"
              placeholder="Enter your password"
              autocomplete="current-password"
            />
          </UFormField>

          <UAlert
            v-if="error"
            color="error"
            variant="soft"
            icon="i-heroicons-exclamation-triangle"
            :title="error"
          />

          <div class="flex justify-end">
            <UButton
              type="submit"
              :loading="isLoading"
              block
            >
              Sign In
            </UButton>
          </div>
        </UForm>

        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-700" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 text-gray-500 bg-white dark:bg-gray-900">
              Or continue with
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-3">
          <UButton
            to="/api/oauth/login/github"
            variant="outline"
            class="w-full"
            icon="i-simple-icons-github"
          >
            GitHub
          </UButton>
        </div>
      </UCard>
    </div>
  </UContainer>
</template>