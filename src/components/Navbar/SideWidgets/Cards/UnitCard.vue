<script setup lang="ts">
import BaseCard from './BaseCard.vue'

interface Props {
  active?: boolean
  grow?: boolean
  title: string
  icon: string
  orientation?: 'row' | 'column'
  color?: string
  value: any | any[]
  unit: string
}

const childProps = defineProps<Props>()
</script>

<template>
  <BaseCard v-bind="childProps">
    <template #default="{ value: val }">
      <span data-testid="card-value" class="text-title-medium font-weight-bold">{{ val }}</span>
      <span data-testid="card-unit" class="text-label-large ml-1">{{ unit }}</span>
    </template>
  </BaseCard>
</template>
