<template>
  <div class="min-h-screen flex">
    <!-- Sidebar -->
    <UNavigationbar class="w-64 p-4 border-r border-gray-200 dark:border-gray-700">
      <template #branding>
        <NuxtLink to="/admin" class="text-xl font-bold">
          Subtly Admin
        </NuxtLink>
      </template>

      <template #default>
        <UVerticalNavigation>
          <UNavigationItem
            label="Dashboard"
            to="/admin"
            icon="i-heroicons-home"
          />
          <UNavigationItem
            label="Users"
            to="/admin/users"
            icon="i-heroicons-users"
          />
          <UNavigationItem
            label="Settings"
            to="/admin/settings"
            icon="i-heroicons-cog-6-tooth"
          />
        </UVerticalNavigation>
      </template>

      <template #footer>
        <ColorScheme>
          <UButton
            color="neutral"
            variant="ghost"
            :icon="$colorMode.preference === 'dark' ? 'i-heroicons-moon' : 'i-heroicons-sun'"
            @click="$colorMode.preference = $colorMode.preference === 'dark' ? 'light' : 'dark'"
            block
          />
        </ColorScheme>
      </template>
    </UNavigationbar>

    <!-- Main Content -->
    <div class="flex-1">
      <div class="p-6">
        <slot />
      </div>
    </div>
  </div>
</template>
