# AuraTorrent Technical Wiki

Welcome to the comprehensive technical documentation for AuraTorrent, a fast open-source WebUI for qBittorrent built on Vue 3 and Vite.

## Table of Contents
1. [Architecture](#architecture)
2. [Features](#features)
3. [Deployment](#deployment)
4. [Security](#security)

---

## Architecture

AuraTorrent is built on a modern, reactive frontend stack designed for speed, low overhead, and deep integration with the qBittorrent Web API.

### Frontend Stack
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Styling**: SCSS + ThemeLab CSS Variables

### State Management & Reactivity
The application state is heavily decentralized into modular Pinia stores:
1. **TorrentStore**: Manages the local cache of torrent objects, applying incremental diffs received from the qBittorrent sync API.
2. **MainDataStore**: Holds global application state, server metrics, and API connection status.
3. **ThemeStore**: Manages the active ThemeLab preset and handles serialization to IndexedDB.

### qBittorrent API Integration
AuraTorrent heavily relies on the `/api/v2/sync/maindata` endpoint. Instead of repeatedly querying all torrents, the frontend maintains a local state tree and only requests incremental changes since the last `rid` (Response ID). This drastically reduces CPU and network overhead for seedboxes with thousands of torrents.

#### Polling Loop
The primary synchronization loop runs inside a Vue composable. It dynamically adjusts its polling frequency based on the window visibility state (using the Page Visibility API) to conserve resources when the PWA is backgrounded.

### PWA & Offline Support
Vite's PWA plugin is utilized to generate a Service Worker that aggressively caches the static assets (`index.html`, JS, CSS). This ensures AuraTorrent loads instantly from disk, even on slow connections, before attempting to fetch the latest torrent data from the API.

---

## Features

### Bandwidth Scheduler Matrix
The Bandwidth Scheduler Matrix visually represents and controls the application's global bandwidth limits across a 7-day, 24-hour cycle. 
- **The Grid (7x24)**: The UI presents a 168-cell matrix representing every hour of the week.
- **Cell States**: Each cell can hold one of three states: `Normal` (Default limits), `Throttled` (Alternative limits), or `Unmetered` (Infinite limits).
- **Tick Evaluation**: A background Vue watcher evaluates the current system time every 60 seconds against the matrix configuration.
- **API Execution**: When a boundary condition is crossed, the frontend dispatches a REST API call to qBittorrent (`POST /api/v2/transfer/toggleSpeedLimitsMode`).

### ThemeLab Engine
The ThemeLab Engine is AuraTorrent's dynamic CSS customization framework. It allows users to modify the visual appearance in real-time.
- **State Persistence**: The `ThemeStore` (Pinia) holds a reactive object representing customizable properties. This state is backed up asynchronously to `IndexedDB` using localforage.
- **DOM Injection**: A Vue watcher observes the `ThemeStore` and dynamically updates the `document.documentElement.style` properties.
- **Glassmorphism**: Adjust `backdrop-filter: blur(Xpx)` and background opacity.
- **Export**: Themes can be exported as JSON payloads.

### Additional Features
- **Global Command Palette**: Press `Cmd/Ctrl + K` to jump to specific settings, perform actions, or search torrents instantly.
- **Global Speed Ticker**: Press `Ctrl+Shift+T` anywhere to summon a floating HUD sparkline graph of I/O speeds.
- **B-I-O-S Easter Egg**: Type `B-I-O-S` on your keyboard to open the BiosSystem Kernel Diagnostic HUD.
- **Telegram Companion Bot (AuraBot)**: Pushes download-complete and error alerts to Telegram and answers `/status` on demand.

---

## Deployment

### Quick Start (Production)
Download the latest release and extract it to your qBittorrent WebUI directory. Enable the custom UI in qBittorrent options and point it to the extracted folder.

### Docker
Run the stack with Docker Compose:
```bash
npm run build
docker compose up -d
```

Pull the standalone, nginx-served published image:
```bash
docker pull ghcr.io/biossystem/auratorrent:latest
docker run -p 8000:80 ghcr.io/biossystem/auratorrent:latest
```

### Developer Setup
1. Clone the repository
2. Run `npm install`
3. Run `npm run dev`
4. Open `http://localhost:5173` and connect to a local qBittorrent instance.

---

## Security

AuraTorrent enforces strict web security boundaries:

- **Enforced Dependency Audit**: CI runs `npm audit` on every pull request and fails the build on any high-severity finding.
- **Strict WebUI Sandboxing**: Enforces restricted API communications and secure CORS configurations.
- **Upstream Parity Security Fixes**: Integrates upstream patches directly from verified VueTorrent pull requests.

Review the `SECURITY.md` for detailed guidelines.
