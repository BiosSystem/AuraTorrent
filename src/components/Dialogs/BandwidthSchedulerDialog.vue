<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDialogStore } from '@/stores'
import { toast } from 'vue3-toastify'

const props = defineProps<{
  guid: string
}>()

const dialogStore = useDialogStore()
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const HOURS = Array.from({ length: 24 }, (_, i) => i)

// 0: normal, 1: slow, 2: stop
const schedule = ref<number[][]>(
  Array.from({ length: 7 }, () => Array(24).fill(0))
)

const isDragging = ref(false)
const dragValue = ref(0)

onMounted(() => {
  const saved = localStorage.getItem('aura_bandwidth_schedule')
  if (saved) {
    try {
      schedule.value = JSON.parse(saved)
    } catch (e) {
      console.error('Failed to parse schedule', e)
    }
  }
})

function saveSchedule() {
  localStorage.setItem('aura_bandwidth_schedule', JSON.stringify(schedule.value))
  toast.success('Bandwidth schedule saved!')
  dialogStore.destroyDialog(props.guid)
}

function handleMousedown(dayIdx: number, hourIdx: number) {
  isDragging.value = true
  dragValue.value = (schedule.value[dayIdx][hourIdx] + 1) % 3
  schedule.value[dayIdx][hourIdx] = dragValue.value
}

function handleMouseenter(dayIdx: number, hourIdx: number) {
  if (isDragging.value) {
    schedule.value[dayIdx][hourIdx] = dragValue.value
  }
}

function handleMouseup() {
  isDragging.value = false
}
</script>

<template>
  <v-dialog :model-value="true" max-width="800" @update:model-value="dialogStore.destroyDialog(props.guid)">
    <v-card class="schedule-dialog" @mouseup="handleMouseup" @mouseleave="handleMouseup">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-calendar-clock" class="mr-2" color="accent" />
        Bandwidth Scheduling Matrix
        <v-spacer />
        <v-btn icon="mdi-close" variant="text" @click="dialogStore.destroyDialog(props.guid)" />
      </v-card-title>
      
      <v-card-text>
        <div class="schedule-legend d-flex mb-4">
          <div class="legend-item mr-4"><div class="legend-box val-0"></div> Normal (Unlimited)</div>
          <div class="legend-item mr-4"><div class="legend-box val-1"></div> Slow (Alt Speed)</div>
          <div class="legend-item"><div class="legend-box val-2"></div> Stop (0 KB/s)</div>
        </div>
        
        <div class="schedule-grid" @dragstart.prevent>
          <div class="grid-header-row">
            <div class="grid-cell empty"></div>
            <div v-for="h in HOURS" :key="`h-${h}`" class="grid-cell hour-label">{{ h }}</div>
          </div>
          
          <div v-for="(day, dIdx) in DAYS" :key="`d-${dIdx}`" class="grid-row">
            <div class="grid-cell day-label">{{ day }}</div>
            <div 
              v-for="h in HOURS" 
              :key="`c-${dIdx}-${h}`"
              class="grid-cell schedule-cell"
              :class="`val-${schedule[dIdx][h]}`"
              @mousedown="handleMousedown(dIdx, h)"
              @mouseenter="handleMouseenter(dIdx, h)"
            ></div>
          </div>
        </div>
        
        <div class="mt-4 text-caption text-grey">
          Click and drag to paint the schedule. The system will automatically apply Alternative Speed Limits or pause traffic based on this matrix.
        </div>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="dialogStore.destroyDialog(props.guid)">Cancel</v-btn>
        <v-btn color="accent" variant="tonal" @click="saveSchedule">Save Schedule</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.schedule-legend {
  font-size: 0.85rem;
}
.legend-item {
  display: flex;
  align-items: center;
}
.legend-box {
  width: 16px;
  height: 16px;
  margin-right: 8px;
  border-radius: 4px;
}

.schedule-grid {
  display: flex;
  flex-direction: column;
  gap: 2px;
  user-select: none;
}
.grid-header-row, .grid-row {
  display: flex;
  gap: 2px;
}
.grid-cell {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
}
.empty { width: 40px; }
.day-label { width: 40px; justify-content: flex-start; font-weight: bold; }
.hour-label { color: rgba(255, 255, 255, 0.5); }

.schedule-cell {
  background: rgba(128, 128, 128, 0.2);
  border-radius: 2px;
  cursor: crosshair;
  transition: transform 0.1s;
}
.schedule-cell:hover {
  transform: scale(1.1);
  z-index: 1;
}

.val-0 { background: rgba(0, 255, 102, 0.6); } /* Normal */
.val-1 { background: rgba(255, 193, 7, 0.6); } /* Slow */
.val-2 { background: rgba(244, 67, 54, 0.6); } /* Stop */

.schedule-dialog {
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
</style>
