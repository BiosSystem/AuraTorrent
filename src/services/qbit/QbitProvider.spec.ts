import type { AxiosAdapter, InternalAxiosRequestConfig } from 'axios'
import { AxiosError } from 'axios'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import QBitProvider from './QbitProvider'

describe('QBitProvider timeout retry behavior', () => {
  const provider = QBitProvider.getInstance()
  const axiosInstance = (provider as unknown as { axios: { defaults: { adapter?: AxiosAdapter } } }).axios
  const originalAdapter = axiosInstance.defaults.adapter

  beforeEach(() => {
    vi.restoreAllMocks()
    axiosInstance.defaults.adapter = originalAdapter
  })

  it('does not retry addTorrents requests on timeout', async () => {
    const adapter = vi.fn((config: InternalAxiosRequestConfig) => Promise.reject(new AxiosError('timeout of 30000ms exceeded', 'ECONNABORTED', config)))
    axiosInstance.defaults.adapter = adapter

    await expect(provider.addTorrents([], 'magnet:?xt=urn:btih:0123456789abcdef')).rejects.toMatchObject({
      code: 'ECONNABORTED',
    })

    expect(adapter).toHaveBeenCalledTimes(1)
  })
})
