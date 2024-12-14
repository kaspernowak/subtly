<script setup lang="ts">
interface TranslationHistory {
  filename: string
  source_lang: string
  target_lang: string
  created_at: string
  status: 'success' | 'error'
}

definePageMeta({
  middleware: ['auth']
})

const isUploading = ref(false)
const selectedFile = ref<File | null>(null)
const targetLanguage = ref('es')
const translations = ref<TranslationHistory[]>([])
const isLoading = ref(true)

const languages = [
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'it', label: 'Italian' },
  { value: 'pt', label: 'Portuguese' },
  { value: 'da', label: 'Danish' },
  { value: 'nl', label: 'Dutch' },
  { value: 'pl', label: 'Polish' }
]

async function loadTranslations() {
  isLoading.value = true
  try {
    const response = await fetch('/api/translation/history')
    translations.value = await response.json()
  } catch (error) {
    useToast().add({
      title: 'Error',
      description: 'Failed to load translation history',
      color: 'error'
    })
  } finally {
    isLoading.value = false
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const files = target.files
  
  if (!files || files.length === 0) {
    selectedFile.value = null
    return
  }
  
  const file = files[0]
  if (file instanceof File) {
    selectedFile.value = file
  } else {
    selectedFile.value = null
  }
}

async function handleUpload() {
  const file = selectedFile.value
  if (!file) {
    useToast().add({
      title: 'Error',
      description: 'Please select a file',
      color: 'error'
    })
    return
  }

  // Validate file type
  if (!file.name.toLowerCase().endsWith('.srt')) {
    useToast().add({
      title: 'Error',
      description: 'Please select a valid SRT subtitle file',
      color: 'error'
    })
    return
  }

  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)
  formData.append('target_language', targetLanguage.value)

  try {
    const response = await fetch('/api/translation/translate', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('Translation failed')
    }

    const result = await response.json()
    useToast().add({
      title: 'Success',
      description: 'Subtitle file translated successfully',
      color: 'success'
    })

    // Refresh translation history
    await loadTranslations()
  } catch (error) {
    useToast().add({
      title: 'Error',
      description: error instanceof Error ? error.message : 'Failed to translate subtitles',
      color: 'error'
    })
  } finally {
    isUploading.value = false
  }
}

// Load translation history on mount
onMounted(() => {
  loadTranslations()
})
</script>

<template>
  <UContainer>
    <UCard>
      <template #header>
        <h1 class="text-2xl font-bold">Translate Subtitles</h1>
      </template>

      <div class="space-y-6">
        <UFormGroup label="Target Language">
          <USelect
            v-model="targetLanguage"
            :options="languages"
            option-attribute="label"
            value-attribute="value"
          />
        </UFormGroup>

        <UFormGroup label="Subtitle File">
          <UInput
            type="file"
            accept=".srt"
            @change="handleFileChange"
          />
          <template #help>
            <span class="text-sm text-gray-500">Only .srt files are supported</span>
          </template>
        </UFormGroup>

        <div class="flex justify-end">
          <UButton
            :loading="isUploading"
            :disabled="!selectedFile"
            @click="handleUpload"
          >
            Translate
          </UButton>
        </div>
      </div>
    </UCard>

    <!-- Translation History -->
    <UCard class="mt-6">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-bold">Translation History</h2>
          <UButton
            icon="i-heroicons-arrow-path"
            variant="ghost"
            :loading="isLoading"
            @click="loadTranslations"
          />
        </div>
      </template>

      <UTable
        :loading="isLoading"
        :rows="translations"
        :columns="[
          {
            accessorKey: 'filename',
            header: 'File'
          },
          {
            accessorKey: 'source_lang',
            header: 'From'
          },
          {
            accessorKey: 'target_lang',
            header: 'To'
          },
          {
            accessorKey: 'created_at',
            header: 'Date'
          },
          {
            accessorKey: 'status',
            header: 'Status'
          }
        ]"
      >
        <template #status-data="{ row }">
          <UBadge
            :color="row.original.status === 'success' ? 'success' : 'error'"
          >
            {{ row.original.status }}
          </UBadge>
        </template>
      </UTable>
    </UCard>
  </UContainer>
</template>
