# Execution Architecture

AuraTorrent is built on a modern, reactive frontend stack designed for speed, low overhead, and deep integration with the qBittorrent Web API.

## Frontend Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Styling**: SCSS + ThemeLab CSS Variables

## State Management & Reactivity

The application state is heavily decentralized into modular Pinia stores:

1. **TorrentStore**: Manages the local cache of torrent objects, applying incremental diffs received from the qBittorrent sync API.
2. **MainDataStore**: Holds global application state, server metrics, and API connection status.
3. **ThemeStore**: Manages the active ThemeLab preset and handles serialization to IndexedDB.

## qBittorrent API Integration

AuraTorrent heavily relies on the `/api/v2/sync/maindata` endpoint. Instead of repeatedly querying all torrents, the frontend maintains a local state tree and only requests incremental changes since the last `rid` (Response ID). This drastically reduces CPU and network overhead for seedboxes with thousands of torrents.

### Polling Loop

The primary synchronization loop runs inside a Vue composable. It dynamically adjusts its polling frequency based on the window visibility state (using the Page Visibility API) to conserve resources when the PWA is backgrounded.

## PWA & Offline Support

Vite's PWA plugin is utilized to generate a Service Worker that aggressively caches the static assets (`index.html`, JS, CSS). This ensures AuraTorrent loads instantly from disk, even on slow connections, before attempting to fetch the latest torrent data from the API.
