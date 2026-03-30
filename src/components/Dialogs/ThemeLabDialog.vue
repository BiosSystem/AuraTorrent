<script setup lang="ts">
import { ref } from 'vue'
import { toast } from 'vue3-toastify'
import { useDialogStore } from '@/stores'

const props = defineProps<{
  guid: string
}>()

const dialogStore = useDialogStore()

const accentColor = ref('#00ff72')
const blurRadius = ref(16)
const glowIntensity = ref(50)

function applyTheme() {
  document.documentElement.style.setProperty('--aura-accent', accentColor.value)
  document.documentElement.style.setProperty('--aura-blur', `${blurRadius.value}px`)
  document.documentElement.style.setProperty('--aura-glow', `${glowIntensity.value}%`)
}

function saveTheme() {
  applyTheme()
  const themeConfig = {
    accent: accentColor.value,
    blur: blurRadius.value,
    glow: glowIntensity.value,
  }
  localStorage.setItem('aura_custom_theme', JSON.stringify(themeConfig))
  toast.success('Theme applied and saved!')
  dialogStore.deleteDialog(props.guid)
}

function exportTheme() {
  const themeConfig = {
    accent: accentColor.value,
    blur: blurRadius.value,
    glow: glowIntensity.value,
  }
  const blob = new Blob([JSON.stringify(themeConfig, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'aura-theme.json'
  a.click()
  URL.revokeObjectURL(url)
  toast.info('Theme exported as JSON.')
}
</script>

<template>
  <v-dialog :model-value="true" max-width="500" @update:model-value="dialogStore.deleteDialog(props.guid)">
    <v-card class="theme-lab-dialog">
      <v-card-title class="d-flex align-center text-primary">
        <v-icon icon="mdi-palette-advanced" class="mr-2" />
        AuraTheme Engine Lab
        <v-spacer />
        <v-btn icon="mdi-close" variant="text" @click="dialogStore.deleteDialog(props.guid)" />
      </v-card-title>

      <v-card-text>
        <v-color-picker v-model="accentColor" hide-canvas hide-inputs show-swatches class="mb-4" @update:model-value="applyTheme"></v-color-picker>

        <div class="text-caption mb-1">Glassmorphism Blur Radius</div>
        <v-slider v-model="blurRadius" min="0" max="40" step="1" thumb-label @update:model-value="applyTheme">
          <template #append>
            <span class="text-caption">{{ blurRadius }}px</span>
          </template>
        </v-slider>

        <div class="text-caption mb-1">Neon Glow Intensity</div>
        <v-slider v-model="glowIntensity" min="0" max="100" step="1" thumb-label @update:model-value="applyTheme">
          <template #append>
            <span class="text-caption">{{ glowIntensity }}%</span>
          </template>
        </v-slider>

        <v-alert type="info" variant="tonal" class="mt-4" density="compact"> AuraTheme changes are applied in real-time. Export as JSON to share with the community! </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-btn variant="text" prepend-icon="mdi-export" @click="exportTheme">Export</v-btn>
        <v-spacer />
        <v-btn variant="text" @click="dialogStore.deleteDialog(props.guid)">Cancel</v-btn>
        <v-btn color="primary" variant="tonal" @click="saveTheme">Save Theme</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.theme-lab-dialog {
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
</style>
