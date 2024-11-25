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
}

const childProps = defineProps<Props>()
</script>

<template>
  <BaseCard v-bind="childProps">
    <template #default="{ value: val }">
      <span class="text-title-medium font-weight-bold">{{ val }}</span>
    </template>
  </BaseCard>
</template>
