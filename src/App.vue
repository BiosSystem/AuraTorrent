<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onBeforeMount, onMounted, ref, watch, watchEffect, onBeforeUnmount } from 'vue'
import { toast } from 'vue3-toastify'
import AddPanel from './components/AddPanel.vue'
import AddTorrentDialog from './components/Dialogs/AddTorrentDialog.vue'
import DnDZone from './components/DnDZone.vue'
import SpeedTicker from './components/SpeedTicker.vue'
import Navbar from './components/Navbar/Navbar.vue'
import Sidebar from './components/Navbar/Sidebar.vue'
import { useBackendSync, useI18nUtils } from './composables'
import { TitleOptions } from './constants/vuetorrent'
import { formatPercent, formatSpeed } from './helpers'
import { backend } from './services/backend'
import {
  useAddTorrentStore,
  useAppStore,
  useDashboardStore,
  useDialogStore,
  useGlobalStore,
  useLogStore,
  useMaindataStore,
  usePreferenceStore,
  useSidebarStore,
  useTorrentStore,
  useVueTorrentStore,
} from './stores'

const { t } = useI18nUtils()
const addTorrentStore = useAddTorrentStore()
const appStore = useAppStore()
const dashboardStore = useDashboardStore()
const dialogStore = useDialogStore()
const logStore = useLogStore()
const sidebarStore = useSidebarStore()
const maindataStore = useMaindataStore()
const { serverState } = storeToRefs(maindataStore)
const torrentStore = useTorrentStore()
const { torrents } = storeToRefs(torrentStore)
const preferencesStore = usePreferenceStore()
const { routerDomKey } = storeToRefs(useGlobalStore())
const vuetorrentStore = useVueTorrentStore()
const { language, uiTitleCustom, uiTitleType, useBitSpeed } = storeToRefs(vuetorrentStore)

const showBiosHud = ref(false)

const backendSyncObjects = [
  useBackendSync(dashboardStore, 'vuetorrent_dashboard', {
    whitelist: ['displayMode'],
  }),
  useBackendSync(torrentStore, 'vuetorrent_torrents', {
    whitelist: ['sortCriterias'],
  }),
  useBackendSync(sidebarStore, 'vuetorrent_sidebarSettings'),
  useBackendSync(vuetorrentStore, 'vuetorrent_webuiSettings', {
    blacklist: ['uiTitleCustom'],
  }),
]

async function checkAuthentication() {
  const authStatus = appStore.fetchAuthStatus()
  const timer = setTimeout(() => {
    toast.loading(t('login.pending'), {
      toastId: 'login-pending',
      onOpen: () => {
        void authStatus.finally(() => toast.remove('login-pending'))
      },
    })
  }, 1000)
  await authStatus.finally(() => clearTimeout(timer))
}

function blockContextMenu(event: Event) {
  if (!event.target) return

  const targetNode = event.target as Element
  if (targetNode.closest('[data-custom-context-menu]')) {
    event.preventDefault()
    return false
  }
}

// PWA file handler
function addLaunchQueueConsumer() {
  const win = window as unknown as {
    launchQueue?: {
      setConsumer: (callback: (launchParams: { files: Readonly<FileSystemFileHandle[]>; targetURL: string }) => void) => void
    }
  }
  win.launchQueue?.setConsumer(launchParams => {
    if (launchParams.files && launchParams.files.length) {
      void Promise.all(launchParams.files.map(async file => addTorrentStore.pushTorrentToQueue(await file.getFile()))).then(() => dialogStore.createDialog(AddTorrentDialog))
    }
  })
}

onBeforeMount(() => {
  vuetorrentStore.updateTheme()
  vuetorrentStore.setLanguage(language.value)
  addLaunchQueueConsumer()

  document.addEventListener('contextmenu', blockContextMenu)
})

onMounted(() => {
  sessionStorage.setItem('vuetorrent_mounted', 'true')

  let keyBuffer = ''
  window.addEventListener('keydown', e => {
    keyBuffer = (keyBuffer + e.key).slice(-4)
    if (keyBuffer.toLowerCase() === 'bios') {
      keyBuffer = ''
      showBiosHud.value = !showBiosHud.value
      toast[showBiosHud.value ? 'success' : 'info'](
        showBiosHud.value ? '⚡ BiosSystem Kernel HUD — Active' : 'HUD Dismissed',
        { toastId: 'bios-hud', autoClose: 2000 }
      )
    }
  })

  void checkAuthentication()
})

onBeforeUnmount(() => {
  document.removeEventListener('contextmenu', blockContextMenu)
})

watch(
  () => appStore.isAuthenticated,
  async isAuthenticated => {
    if (isAuthenticated) {
      maindataStore.forceMaindataSync()
      await preferencesStore.fetchPreferences()
      await logStore.cleanAndFetchLogs()

      void backend.ping().then(async ok => {
        if (ok) {
          await Promise.allSettled(backendSyncObjects.map(obj => obj.loadState()))
          backendSyncObjects.forEach(obj => obj.registerWatcher())
        }
      })
    } else {
      maindataStore.stopMaindataSync()
      backendSyncObjects.forEach(obj => obj.cancelWatcher())
    }
  },
  {
    immediate: true,
  }
)

watchEffect(() => {
  const appInstanceName = preferencesStore.preferences?.app_instance_name
  const baseName = appInstanceName && appInstanceName.length ? appInstanceName : 'AuraTorrent'

  const mode = uiTitleType.value
  switch (mode) {
    case TitleOptions.GLOBAL_SPEED: {
      const dl_speed = formatSpeed(serverState.value?.dl_info_speed ?? 0, useBitSpeed.value)
      const ul_speed = formatSpeed(serverState.value?.up_info_speed ?? 0, useBitSpeed.value)
      document.title = `[D: ${dl_speed}, U: ${ul_speed}] ${baseName}`
      break
    }
    case TitleOptions.FIRST_TORRENT_STATUS: {
      const torrent = torrents.value.at(0)
      if (torrent) {
        const dl_speed = formatSpeed(torrent.dlspeed, useBitSpeed.value)
        const ul_speed = formatSpeed(torrent.upspeed, useBitSpeed.value)
        const progress = formatPercent(torrent.progress)
        document.title = `[D: ${dl_speed}, U: ${ul_speed}, ${progress}] ${baseName}`
      } else {
        document.title = `[N/A] ${baseName}`
      }
      break
    }
    case TitleOptions.CUSTOM:
      document.title = uiTitleCustom.value
      break
    case TitleOptions.DEFAULT:
      document.title = baseName
      break
  }
})
</script>

<template>
  <v-app class="text-noselect">
    <component :is="dialog.component" v-for="dialog in dialogStore.dialogs.values()" :key="dialog.guid" v-bind="{ guid: dialog.guid, ...dialog.props }" />
    
    <Transition name="bios-fade">
      <div v-if="showBiosHud" class="bios-diagnostic-hud" @click="showBiosHud = false">
        <div class="bios-hud-scanline" />
        <div class="bios-hud-header">
          <span class="bios-hud-badge">⚡</span>
          BIOSYSTEM KERNEL DIAGNOSTIC
          <span class="bios-hud-badge">⚡</span>
        </div>
        <div class="bios-hud-grid">
          <div class="bios-hud-cell">
            <span class="bios-hud-label">KERNEL</span>
            <span class="bios-hud-value bios-hud-value--ok">VALIDATED</span>
          </div>
          <div class="bios-hud-cell">
            <span class="bios-hud-label">ENCRYPTION</span>
            <span class="bios-hud-value bios-hud-value--ok">AES-256</span>
          </div>
          <div class="bios-hud-cell">
            <span class="bios-hud-label">TORRENTS</span>
            <span class="bios-hud-value">{{ torrents.length }}</span>
          </div>
          <div class="bios-hud-cell">
            <span class="bios-hud-label">↓ DOWNLOAD</span>
            <span class="bios-hud-value bios-hud-value--dl">{{ formatSpeed(serverState?.dl_info_speed ?? 0, useBitSpeed) }}</span>
          </div>
          <div class="bios-hud-cell">
            <span class="bios-hud-label">↑ UPLOAD</span>
            <span class="bios-hud-value bios-hud-value--ul">{{ formatSpeed(serverState?.up_info_speed ?? 0, useBitSpeed) }}</span>
          </div>
          <div class="bios-hud-cell">
            <span class="bios-hud-label">ENGINE</span>
            <span class="bios-hud-value">VUE 3 + VITE</span>
          </div>
        </div>
        <div class="bios-hud-footer">BiosSystem Open Source Community — click to dismiss</div>
      </div>
    </Transition>

    <Sidebar v-if="appStore.isAuthenticated" />
    <Navbar v-if="appStore.isAuthenticated" />
    <v-main>
      <router-view :key="routerDomKey" />
    </v-main>
    <AddPanel v-if="appStore.isAuthenticated" />
    <DnDZone />
    <SpeedTicker v-if="appStore.isAuthenticated" />
  </v-app>
</template>

<style scoped>
.bios-diagnostic-hud {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 92%;
  max-width: 620px;
  background: rgba(4, 10, 20, 0.97);
  border: 1px solid rgba(0, 255, 102, 0.5);
  box-shadow:
    0 0 0 1px rgba(0, 255, 102, 0.12),
    0 0 40px rgba(0, 255, 102, 0.2),
    0 24px 60px rgba(0, 0, 0, 0.7);
  border-radius: 18px;
  z-index: 999999;
  padding: 28px 32px 22px;
  color: #00ff72;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  backdrop-filter: blur(24px) saturate(180%);
  cursor: pointer;
  overflow: hidden;
  animation: biosPulse 3s ease-in-out infinite alternate;
}

.bios-hud-scanline {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 3px,
    rgba(0, 0, 0, 0.12) 3px,
    rgba(0, 0, 0, 0.12) 4px
  );
  pointer-events: none;
  border-radius: 18px;
}

.bios-hud-header {
  font-size: 1.05rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 22px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(0, 255, 102, 0.25);
  letter-spacing: 3px;
  color: #00ff72;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.bios-hud-badge {
  font-size: 1.1rem;
  animation: badgeSpin 4s linear infinite;
  display: inline-block;
}

.bios-hud-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 14px;
  margin-bottom: 20px;
}

.bios-hud-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: rgba(0, 255, 102, 0.05);
  border: 1px solid rgba(0, 255, 102, 0.12);
  border-radius: 10px;
  padding: 10px 14px;
}

.bios-hud-label {
  font-size: 0.62rem;
  letter-spacing: 2px;
  color: rgba(0, 255, 102, 0.5);
  text-transform: uppercase;
}

.bios-hud-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #00ff72;

  &--ok { color: #00ff72; }
  &--dl { color: #00d4ff; }
  &--ul { color: #a78bfa; }
}

.bios-hud-footer {
  text-align: center;
  font-size: 0.72rem;
  opacity: 0.4;
  letter-spacing: 1px;
  margin-top: 6px;
}

.bios-fade-enter-active,
.bios-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.bios-fade-enter-from,
.bios-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, calc(-50% - 12px)) scale(0.96);
}

@keyframes biosPulse {
  from { box-shadow: 0 0 24px rgba(0, 255, 102, 0.15), 0 24px 60px rgba(0,0,0,0.7); }
  to   { box-shadow: 0 0 50px rgba(0, 255, 102, 0.35), 0 24px 60px rgba(0,0,0,0.7); }
}

@keyframes badgeSpin {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
