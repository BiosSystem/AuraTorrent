import { useIntervalFn } from '@vueuse/core'
import { isAxiosError } from 'axios'
import { acceptHMRUpdate, defineStore, storeToRefs } from 'pinia'
import { ref, shallowRef } from 'vue'
import { useTask } from 'vue-concurrency'
import { toast } from 'vue3-toastify'
import { useAppStore } from './app'
import { useVueTorrentStore } from './vuetorrent'
import qbit from '@/services/qbit'
import { ServerState } from '@/types/qbit/models'
import { isFullUpdate } from '@/types/qbit/responses'

export const useMaindataStore = defineStore('maindata', () => {
  const rid = ref<number>()
  const serverState = shallowRef<Partial<ServerState>>()
  const reconnectAttempts = ref(0)

  const rawPayload = shallowRef<any>()

  const appStore = useAppStore()
  const vueTorrentStore = useVueTorrentStore()
  const { refreshInterval } = storeToRefs(vueTorrentStore)

  const maindataTask = useTask(function* () {
    yield updateMaindata()
  }).drop()

  const { resume: forceMaindataSync, pause: stopMaindataSync } = useIntervalFn(() => void maindataTask.perform(), refreshInterval, {
    immediate: false,
    immediateCallback: true,
  })

  function syncFromMaindata(fullUpdate: boolean, obj?: Partial<ServerState>) {
    if (fullUpdate) {
      serverState.value = obj
    } else if (obj) {
      serverState.value = { ...serverState.value, ...obj }
    }
  }

  async function updateMaindata() {
    try {
      const response = await qbit.getMaindata(rid.value)
      rid.value = response.rid

      if (reconnectAttempts.value > 0) {
        toast.success('Connection restored! Full sync complete.', { toastId: 'reconnect-success' })
        reconnectAttempts.value = 0
      }

      rawPayload.value = response

      if (isFullUpdate(response)) {
        syncFromMaindata(true, response.server_state)
        return
      }

      syncFromMaindata(false, response.server_state)
    } catch (error: unknown) {
      if (isAxiosError(error) && error.response?.status === 403) {
        console.error('No longer authenticated, logging out...')
        await appStore.setAuthStatus(false)
        await vueTorrentStore.redirectToLogin()
      } else {
        console.error('Maindata sync failed:', error)
        reconnectAttempts.value++
        const backoffSeconds = Math.min(5 * reconnectAttempts.value, 30)
        toast.warning(`Connection lost. Retrying in ${backoffSeconds}s (Attempt ${reconnectAttempts.value})...`, { toastId: 'reconnect-warning', autoClose: backoffSeconds * 1000 })
        rid.value = undefined
      }
    }
  }

  async function syncTorrentPeers(hash: string, rid?: number) {
    return await qbit.syncTorrentPeers(hash, rid)
  }

  async function addTorrentPeers(hash: string, peers: string[]) {
    await qbit.addTorrentPeers([hash], peers)
  }

  async function banPeers(peers: string[]) {
    await qbit.banPeers(peers)
  }

  async function setDownloadLimit(limit: number, hashes: string[]) {
    return await qbit.setDownloadLimit(hashes, limit)
  }

  async function setUploadLimit(limit: number, hashes: string[]) {
    return await qbit.setUploadLimit(hashes, limit)
  }

  async function setShareLimit(hashes: string[], ratioLimit: number, seedingTimeLimit: number, inactiveSeedingTimeLimit: number) {
    return await qbit.setShareLimit(hashes, ratioLimit, seedingTimeLimit, inactiveSeedingTimeLimit)
  }

  return {
    rid,
    serverState,
    rawPayload,
    syncTorrentPeers,
    addTorrentPeers,
    banPeers,
    setDownloadLimit,
    setUploadLimit,
    setShareLimit,
    forceMaindataSync,
    stopMaindataSync,
    $reset: () => {
      stopMaindataSync()
      maindataTask.clear()
      rid.value = undefined
      serverState.value = {}
    },
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMaindataStore, import.meta.hot))
}
