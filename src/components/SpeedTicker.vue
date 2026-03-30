<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { formatSpeed } from '@/helpers'
import { useMaindataStore } from '@/stores/maindata'
import { useVueTorrentStore } from '@/stores/vuetorrent'

const maindataStore = useMaindataStore()
const { serverState } = storeToRefs(maindataStore)
const vuetorrentStore = useVueTorrentStore()
const { useBitSpeed } = storeToRefs(vuetorrentStore)

const isVisible = ref(false)

const GRAPH_SIZE = 40
const dlHistory = ref<number[]>(new Array(GRAPH_SIZE).fill(0))
const ulHistory = ref<number[]>(new Array(GRAPH_SIZE).fill(0))
const maxSpeed = ref(1)

function handleKeydown(e: KeyboardEvent) {
  if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 't') {
    isVisible.value = !isVisible.value
  }
}

watch(
  () => serverState.value,
  state => {
    if (!isVisible.value) return

    const dl = state?.dl_info_speed ?? 0
    const ul = state?.up_info_speed ?? 0

    dlHistory.value.shift()
    dlHistory.value.push(dl)

    ulHistory.value.shift()
    ulHistory.value.push(ul)

    const currentMax = Math.max(...dlHistory.value, ...ulHistory.value, 1)
    maxSpeed.value = currentMax
  },
  { deep: true }
)

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
})

function getPath(data: number[]) {
  if (data.length === 0) return ''
  const width = 200
  const height = 40
  const stepX = width / (GRAPH_SIZE - 1)

  return data
    .map((val, i) => {
      const x = i * stepX
      const y = height - (val / maxSpeed.value) * height
      return `${i === 0 ? 'M' : 'L'} ${x} ${y}`
    })
    .join(' ')
}
</script>

<template>
  <Transition name="ticker-fade">
    <div v-if="isVisible" class="speed-ticker-hud" data-custom-context-menu="true">
      <div class="ticker-header">
        <span class="ticker-title">⚡ AURA TICKER</span>
      </div>

      <div class="ticker-stats">
        <div class="stat-col">
          <div class="stat-label dl-label">↓ DL</div>
          <div class="stat-value">{{ formatSpeed(serverState?.dl_info_speed ?? 0, useBitSpeed) }}</div>
        </div>
        <div class="stat-col">
          <div class="stat-label ul-label">↑ UL</div>
          <div class="stat-value">{{ formatSpeed(serverState?.up_info_speed ?? 0, useBitSpeed) }}</div>
        </div>
      </div>

      <div class="ticker-graph-container">
        <svg class="ticker-svg" viewBox="0 0 200 40" preserveAspectRatio="none">
          <path :d="getPath(dlHistory)" class="dl-path" fill="none" stroke-width="2" />
          <path :d="getPath(ulHistory)" class="ul-path" fill="none" stroke-width="2" />
        </svg>
      </div>

      <div class="ticker-hint">Ctrl+Shift+T to dismiss</div>
    </div>
  </Transition>
</template>

<style scoped>
.speed-ticker-hud {
  position: fixed;
  top: 80px;
  right: 24px;
  width: 240px;
  background: rgba(10, 15, 25, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 16px;
  z-index: 999999;
  backdrop-filter: blur(16px) saturate(180%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  pointer-events: none; /* Let clicks pass through */
}

.ticker-header {
  font-size: 0.75rem;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 8px;
}

.ticker-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-col {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.dl-label {
  color: #00d4ff;
}
.ul-label {
  color: #a78bfa;
}

.stat-value {
  font-size: 0.9rem;
  font-weight: bold;
  color: #fff;
}

.ticker-graph-container {
  width: 100%;
  height: 40px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
}

.ticker-svg {
  width: 100%;
  height: 100%;
}

.dl-path {
  stroke: #00d4ff;
}
.ul-path {
  stroke: #a78bfa;
}

.ticker-hint {
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.4);
  text-align: right;
  margin-top: 8px;
}

.ticker-fade-enter-active,
.ticker-fade-leave-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.ticker-fade-enter-from,
.ticker-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
