<script setup lang="ts">
import { onMounted } from 'vue'
import { useDialogStore, useRssStore } from '@/stores'
import RssFeedDialog from '@/components/Dialogs/RssFeedDialog.vue'
import RssRuleDialog from '@/components/Dialogs/RssRuleDialog.vue'

const rssStore = useRssStore()
const dialogStore = useDialogStore()

onMounted(() => {
  rssStore.fetchFeedsTask.perform()
  rssStore.fetchRulesTask.perform()
})

function openAddFeed() {
  dialogStore.createDialog(RssFeedDialog)
}

function openAddRule() {
  dialogStore.createDialog(RssRuleDialog)
}
</script>

<template>
  <v-card class="mb-4 rss-manager" elevation="1">
    <v-card-title class="d-flex justify-space-between align-center">
      <span>{{ $t('rssManager.title', 'RSS Feed Manager') }}</span>
      <div>
        <v-btn color="primary" variant="tonal" size="small" class="mr-2" @click="openAddFeed">
          <v-icon start>mdi-plus</v-icon> Add Feed
        </v-btn>
        <v-btn color="secondary" variant="tonal" size="small" @click="openAddRule">
          <v-icon start>mdi-filter</v-icon> Add Rule
        </v-btn>
      </div>
    </v-card-title>
    
    <v-divider />
    
    <v-card-text>
      <v-row>
        <v-col cols="12" md="6">
          <div class="text-subtitle-1 font-weight-bold mb-2">Active Feeds</div>
          <v-list density="compact" v-if="rssStore.feeds.length">
            <v-list-item v-for="feed in rssStore.feeds" :key="feed.uid" :title="feed.name" :subtitle="feed.url">
              <template #append>
                <v-btn icon="mdi-refresh" variant="text" size="small" @click="rssStore.refreshFeed(feed.name)" />
                <v-btn icon="mdi-delete" variant="text" color="error" size="small" @click="rssStore.deleteFeed(feed.name)" />
              </template>
            </v-list-item>
          </v-list>
          <div v-else class="text-caption text-medium-emphasis">No feeds configured.</div>
        </v-col>
        <v-col cols="12" md="6">
          <div class="text-subtitle-1 font-weight-bold mb-2">Auto-Download Rules</div>
          <v-list density="compact" v-if="rssStore.rules.length">
            <v-list-item v-for="rule in rssStore.rules" :key="rule.name" :title="rule.name" :subtitle="rule.mustContain">
              <template #append>
                <v-btn icon="mdi-delete" variant="text" color="error" size="small" @click="rssStore.deleteRule(rule.name)" />
              </template>
            </v-list-item>
          </v-list>
          <div v-else class="text-caption text-medium-emphasis">No rules configured.</div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
