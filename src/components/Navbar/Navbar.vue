<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import ActiveFilters from './TopWidgets/ActiveFilters.vue'
import TopContainer from './TopWidgets/TopContainer.vue'
import TorrentSearchbar from '@/components/TorrentSearchbar.vue'
import qbit from '@/services/qbit'
import { useNavbarStore, useAppStore } from '@/stores'

const router = useRouter()
const appStore = useAppStore()
const { isDrawerOpen } = storeToRefs(useNavbarStore())

const servers = ref([
  { label: 'Local NAS', url: '' },
  { label: 'Cloud Seedbox', url: 'https://seedbox.example.com/api/v2' },
])

const activeServer = ref(Number(localStorage.getItem('auratorrent_active_server_idx') || '0'))
const switcherOpen = ref(false)

const activeLabel = computed(() => servers.value[activeServer.value]?.label ?? 'Local NAS')

function toggleDrawer() {
  isDrawerOpen.value = !isDrawerOpen.value
}

function goHome() {
  void router.push({ name: 'dashboard' })
}

function selectServer(idx: number) {
  activeServer.value = idx
  localStorage.setItem('auratorrent_active_server_idx', String(idx))
  switcherOpen.value = false

  const server = servers.value[idx]
  qbit.setBaseURL(server.url)

  // Log out and reload to trigger login dialog for the new host
  void appStore.logout().then(() => {
    window.location.reload()
  })
}

function handleKeydown(e: KeyboardEvent) {
  if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'm') {
    e.preventDefault()
    switcherOpen.value = !switcherOpen.value
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <v-app-bar class="ios-padding">
    <v-app-bar-nav-icon @click="toggleDrawer" />

    <div class="title-wrapper cursor-pointer" @click="goHome">
      <span v-if="$vuetify.display.smAndUp" class="text-accent">Aura</span>
      <span v-if="$vuetify.display.smAndUp">Torrent</span>
    </div>

    <!-- Multi-Daemon Server Switcher -->
    <div v-if="$vuetify.display.mdAndUp" class="daemon-switcher ml-4" @click="switcherOpen = !switcherOpen">
      <span class="daemon-switcher__dot" />
      {{ activeLabel }}
      <v-icon size="14" class="ml-1">mdi-chevron-down</v-icon>

      <div v-if="switcherOpen" class="daemon-menu">
        <div v-for="(server, idx) in servers" :key="idx" class="daemon-menu__item" :class="{ 'daemon-menu__item--active': idx === activeServer }" @click.stop="selectServer(idx)">
          <span class="daemon-menu__dot" :class="idx === activeServer ? 'daemon-menu__dot--active' : ''" />
          {{ server.label }}
        </div>
      </div>
    </div>

    <ActiveFilters />

    <TorrentSearchbar v-if="$vuetify.display.lgAndUp" bg-color="background" class="px-6" />
    <v-spacer v-else />

    <TopContainer />
  </v-app-bar>
</template>

<style scoped lang="scss">
.title-wrapper {
  display: inline-flex;
  width: min-content;
  padding: 0.4em;
  align-items: center;
  font-size: larger;
  font-weight: 700;
}

.daemon-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  min-width: 180px;
  background: rgba(8, 12, 26, 0.97);
  border: 1px solid rgba(0, 212, 255, 0.22);
  border-radius: 14px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(0, 212, 255, 0.06);
  backdrop-filter: blur(20px);
  overflow: hidden;
  z-index: 9999;
  animation: menuFadeIn 0.15s ease;
}

.daemon-menu__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: rgba(0, 212, 255, 0.08);
    color: #fff;
  }

  &--active {
    color: #00d4ff;
    font-weight: 600;
  }
}

.daemon-menu__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  flex-shrink: 0;

  &--active {
    background: #00d4ff;
    box-shadow: 0 0 8px #00d4ff;
  }
}

@keyframes menuFadeIn {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
