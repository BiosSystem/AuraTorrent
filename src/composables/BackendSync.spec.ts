import { createPinia, defineStore, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { useBackendSync } from './BackendSync'

const remote = new Map<string, string>()

vi.mock('@/services/backend', () => ({
  backend: {
    get: vi.fn((key: string) => Promise.resolve(remote.get(key) ?? null)),
    set: vi.fn((key: string, value: string) => {
      remote.set(key, value)
      return Promise.resolve(true)
    }),
  },
}))

const useSettingsStore = defineStore('backendSyncSpec', {
  state: () => ({ theme: 'dark', language: 'en' }),
})

describe('useBackendSync', () => {
  beforeEach(() => {
    remote.clear()
    setActivePinia(createPinia())
  })

  it('loads state from its own key', async () => {
    remote.set('auratorrent_webuiSettings', JSON.stringify({ theme: 'light' }))
    const store = useSettingsStore()

    await useBackendSync(store, 'auratorrent_webuiSettings', { legacyKey: 'vuetorrent_webuiSettings' }).loadState()

    expect(store.theme).toBe('light')
  })

  it('imports once from the legacy key and saves under the new key', async () => {
    remote.set('vuetorrent_webuiSettings', JSON.stringify({ theme: 'light', language: 'fr' }))
    const store = useSettingsStore()

    await useBackendSync(store, 'auratorrent_webuiSettings', { legacyKey: 'vuetorrent_webuiSettings' }).loadState()

    expect(store.theme).toBe('light')
    expect(store.language).toBe('fr')
    expect(JSON.parse(remote.get('auratorrent_webuiSettings')!)).toEqual({ theme: 'light', language: 'fr' })
    expect(remote.has('vuetorrent_webuiSettings')).toBe(true)
  })

  it('ignores the legacy key once the new key has data', async () => {
    remote.set('auratorrent_webuiSettings', JSON.stringify({ theme: 'light' }))
    remote.set('vuetorrent_webuiSettings', JSON.stringify({ theme: 'blue' }))
    const store = useSettingsStore()

    await useBackendSync(store, 'auratorrent_webuiSettings', { legacyKey: 'vuetorrent_webuiSettings' }).loadState()

    expect(store.theme).toBe('light')
    expect(JSON.parse(remote.get('vuetorrent_webuiSettings')!)).toEqual({ theme: 'blue' })
  })

  it('writes defaults under the new key when neither key has data', async () => {
    const store = useSettingsStore()

    await useBackendSync(store, 'auratorrent_webuiSettings', { legacyKey: 'vuetorrent_webuiSettings' }).loadState()

    expect(JSON.parse(remote.get('auratorrent_webuiSettings')!)).toEqual({ theme: 'dark', language: 'en' })
    expect(remote.has('vuetorrent_webuiSettings')).toBe(false)
  })

  it('applies the whitelist to imported legacy data', async () => {
    remote.set('vuetorrent_dashboard', JSON.stringify({ theme: 'light', language: 'fr' }))
    const store = useSettingsStore()

    await useBackendSync(store, 'auratorrent_dashboard', { whitelist: ['theme'], legacyKey: 'vuetorrent_dashboard' }).loadState()

    expect(store.theme).toBe('light')
    expect(store.language).toBe('en')
    expect(JSON.parse(remote.get('auratorrent_dashboard')!)).toEqual({ theme: 'light' })
  })
})
