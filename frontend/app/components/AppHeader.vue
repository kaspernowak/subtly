<script setup lang="ts">
const authStore = useAuthStore()
const route = useRoute()

const navLinks = [
  { to: '/dashboard', text: 'Dashboard', requiresAuth: true },
  { to: '/translate', text: 'Translate', requiresAuth: true }
]

const profileMenuItems = [
  { 
    label: 'Profile Settings',
    icon: 'i-heroicons-user',
    to: '/profile'
  },
  {
    label: 'Logout',
    icon: 'i-heroicons-power',
    click: () => authStore.logout()
  }
]

const colorModeItems = ref([
  { 
    label: 'System', 
    value: 'system', 
    icon: 'i-heroicons-computer-desktop' },
  { 
    label: 'Light', 
    value: 'light', 
    icon: 'i-heroicons-sun' },
  { 
    label: 'Dark', 
    value: 'dark', 
    icon: 'i-heroicons-moon' }
])
const value = ref(colorModeItems.value[0]?.value)

const icon = computed(() => colorModeItems.value.find(item => item.value === value.value)?.icon)
</script>

<template>
  <div class="flex h-16 items-center justify-between">
    <!-- Left side -->
    <div class="flex-shrink-0">
      <NuxtLink to="/" class="text-2xl font-bold text-primary hover:text-primary-emphasis transition-colors">
        Subtly
      </NuxtLink>
    </div>

    <!-- Right side -->
    <div class="flex items-center space-x-4">
      <template v-if="authStore.isAuthenticated">
        <div class="hidden md:flex items-center space-x-4">
          <NuxtLink
            v-for="link in navLinks.filter(l => l.requiresAuth)"
            :key="link.to"
            :to="link.to"
            :class="[
              'px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === link.to
                ? 'text-primary dark:text-primary-emphasis'
                : 'text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary-emphasis'
            ]"
          >
            {{ link.text }}
          </NuxtLink>
        </div>

        <UDropdownMenu :items="profileMenuItems">
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-heroicons-user-circle"
          />
        </UDropdownMenu>
      </template>
      <template v-else>
        <UButton
          to="/login"
          icon="i-heroicons-arrow-right-on-rectangle"
        >
          Login
        </UButton>
      </template>

      <ColorScheme>
        <UTooltip :text="`Switch to ${$colorMode.value === 'dark' ? 'light' : 'dark'} mode`">
          <UButton
            :icon="$colorMode.value === 'dark' ? 'i-heroicons-sun' : 'i-heroicons-moon'"
            color="primary"
            class="cursor-pointer"
            variant="ghost"
            size="md"
            @click="$colorMode.preference = $colorMode.value === 'dark' ? 'light' : 'dark'"
          />
        </UTooltip>
        <template #placeholder>
          <div class="w-8 h-8"></div>
        </template>
      </ColorScheme>
    </div>
  </div>
</template>
