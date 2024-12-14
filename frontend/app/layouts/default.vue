<template>
  <UCard class="min-h-screen rounded-none border-0">
    <template #header>
      <AppHeader />
    </template>

    <slot />

    <template #footer>
      <AppFooter />
    </template>
  </UCard>
</template>
