<script setup lang="ts">
import BaseCard from './BaseCard.vue'
import { formatDataUnit, formatDataValue } from '@/helpers'
import { useVueTorrentStore } from '@/stores'

interface Props {
  active?: boolean
  grow?: boolean
  title: string
  icon: string
  orientation?: 'row' | 'column'
  color?: string
  value: number | number[]
}

const childProps = defineProps<Props>()

const vueTorrentStore = useVueTorrentStore()
</script>

<template>
  <BaseCard v-bind="childProps">
    <template #default="{ value: val }">
      <span data-testid="card-value" class="text-title-medium font-weight-bold">{{ formatDataValue(val, vueTorrentStore.useBinarySize) }}</span>
      <span data-testid="card-unit" class="text-label-large ml-1">{{ formatDataUnit(val, vueTorrentStore.useBinarySize) }}</span>
    </template>
  </BaseCard>
</template>
