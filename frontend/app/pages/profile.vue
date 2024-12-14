<script setup lang="ts">
definePageMeta({
  middleware: ['auth']
})

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const stats = [
  { label: 'Videos Translated', value: '12', icon: 'i-heroicons-video-camera' },
  { label: 'Languages Used', value: '5', icon: 'i-heroicons-language' },
  { label: 'Total Minutes', value: '180', icon: 'i-heroicons-clock' }
]
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <div class="flex items-center space-x-4">
          <UAvatar
            :src="`https://api.dicebear.com/7.x/initials/svg?seed=${user?.email}`"
            :alt="user?.full_name || user?.email"
            size="lg"
          />
          <div>
            <h1 class="text-2xl font-bold">{{ user?.full_name || user?.email }}</h1>
            <p class="text-gray-500">{{ user?.email }}</p>
          </div>
        </div>
      </template>

      <div class="grid md:grid-cols-3 gap-6 mt-6">
        <UCard
          v-for="stat in stats"
          :key="stat.label"
          class="text-center"
        >
          <UIcon
            :name="stat.icon"
            class="w-8 h-8 mx-auto mb-2 text-primary"
          />
          <div class="text-2xl font-bold">{{ stat.value }}</div>
          <div class="text-sm text-gray-500">{{ stat.label }}</div>
        </UCard>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-2">
          <UButton
            color="neutral"
            variant="soft"
            icon="i-heroicons-pencil"
          >
            Edit Profile
          </UButton>
          <UButton
            color="error"
            variant="soft"
            icon="i-heroicons-power"
            @click="authStore.logout"
          >
            Logout
          </UButton>
        </div>
      </template>
    </UCard>
  </UContainer>
</template>
