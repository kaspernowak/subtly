<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <div class="flex h-16 items-center justify-between">
    <!-- Left side -->
    <div class="text-sm text-gray-500 dark:text-gray-400">
      {{ currentYear }} Subtly. All rights reserved.
    </div>

    <!-- Right side -->
    <div class="flex items-center space-x-4">
      <UButton icon="i-uil-github" to="https://github.com/kaspernowak/subtly" target="_blank">
        GitHub
      </UButton>
    </div>
  </div>
</template>
