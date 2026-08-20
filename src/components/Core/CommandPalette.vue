<template>
  <v-dialog v-model="isOpen" max-width="600" :scrim="true" transition="dialog-fade-transition">
    <v-card rounded="xl" elevation="24" class="command-palette-card">
      <v-autocomplete
        v-model="search"
        :items="commands"
        item-title="title"
        item-value="id"
        return-object
        autofocus
        clearable
        hide-details
        hide-no-data
        placeholder="Search commands, torrents, or settings..."
        prepend-inner-icon="mdi-magnify"
        variant="solo"
        flat
        class="command-palette-input"
        @update:model-value="onSelect">
        <template #item="{ props, item }">
          <v-list-item v-bind="props" :prepend-icon="(item as any).raw.icon" :title="(item as any).raw.title">
            <template v-if="(item as any).raw.shortcut" #append>
              <v-chip size="x-small" variant="flat" color="grey-darken-3">{{ (item as any).raw.shortcut }}</v-chip>
            </template>
          </v-list-item>
        </template>
      </v-autocomplete>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const isOpen = ref(false)
const search = ref(null)
const router = useRouter()

// Define available commands
const commands = [
  { id: 'home', title: 'Go to Dashboard', icon: 'mdi-view-dashboard', action: () => router.push('/') },
  { id: 'settings', title: 'Open Settings', icon: 'mdi-cog', action: () => router.push('/settings') },
  { id: 'settings-speed', title: 'Settings: Speed Limits', icon: 'mdi-speedometer', action: () => router.push('/settings?tab=speed') },
  { id: 'settings-connection', title: 'Settings: Connection', icon: 'mdi-network', action: () => router.push('/settings?tab=connection') },
  { id: 'rss', title: 'Open RSS Feeds', icon: 'mdi-rss', action: () => router.push('/rss') },
  { id: 'search', title: 'Torrent Search Engine', icon: 'mdi-search-web', action: () => router.push('/search') },
  { id: 'logs', title: 'System Logs', icon: 'mdi-file-document-multiple', action: () => router.push('/logs') },
]

function onSelect(item: any) {
  if (item && item.action) {
    item.action()
  }
  search.value = null
  isOpen.value = false
}

function handleKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    isOpen.value = !isOpen.value
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.command-palette-card {
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.command-palette-input :deep(.v-field__input) {
  font-size: 1.25rem;
  padding-top: 16px;
  padding-bottom: 16px;
}
</style>
