<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&weight=bold&size=34&duration=3000&pause=1000&color=00FF72&center=true&vCenter=true&width=435&lines=AuraTorrent;Next-Gen+WebUI;BiosSystem+Kernel" alt="AuraTorrent Typing Title" />
</p>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=vue,ts,vite,html,css" alt="Tech Stack" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/BiosSystem/AuraTorrent?color=00ff72&style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/qBittorrent-4.4%2B-blue?style=flat-square" alt="qBittorrent">
  <img src="https://img.shields.io/github/license/BiosSystem/AuraTorrent?style=flat-square" alt="License">
</p>

---

**AuraTorrent** is a beautiful, lightning-fast Open Source WebUI for qBittorrent. Built on Vue 3 and Vite, it reimagines the seedbox experience with dynamic scheduling, real-time telemetry HUDs, and deep customization. 

<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/docs/screenshots/screenshot-desktop-dark-mode.png" width="800" alt="Screenshot Desktop" />
</p>

## ✨ Why It's Unique

Unlike standard qBittorrent WebUIs, AuraTorrent includes next-gen features designed for power users:

- **Bandwidth Scheduling Matrix**: A 7×24 visual heatmap grid to paint your bandwidth schedule visually. The UI automatically throttles qBittorrent based on the current hour.
- **AuraTheme Engine**: A live, built-in CSS variable editor. Adjust glassmorphism blur, neon glow intensity, and accent colors in real-time, then export to JSON.
- **Global Speed Ticker**: Press `Ctrl+Shift+T` anywhere to summon a floating, always-on-top HUD sparkline graph of your current I/O speeds.
- **The B-I-O-S Easter Egg**: Type `B-I-O-S` on your keyboard to unlock the BiosSystem Kernel Diagnostic HUD.

## 🎯 Feature Matrix

| Feature | AuraTorrent | VueTorrent | Default UI |
|---|:---:|:---:|:---:|
| **Mobile PWA Support** | ✅ | ✅ | ❌ |
| **Multi-Daemon Switcher** | ✅ | ❌ | ❌ |
| **Visual Bandwidth Heatmap** | ✅ | ❌ | ❌ |
| **Live Theme Editor Lab** | ✅ | ❌ | ❌ |

## 📦 Platform Device Matrix

AuraTorrent is responsive across all devices and installs directly into qBittorrent without additional daemons.

| Platform | Support | Notes |
|---|:---:|---|
| **Windows / macOS / Linux** | 🟢 Native | Works in any modern desktop browser (Chrome, Edge, Firefox, Safari). |
| **iOS / iPadOS** | 🟢 PWA | Add to Home Screen for a native app-like experience without App Store limits. |
| **Android** | 🟢 PWA | Install via Chrome. Handles `magnet:` links directly. |
| **Docker / Seedboxes** | 🟢 Supported | Drop the files into your container's WebUI folder or mount via volume. |

## 🚀 Quick Start

Drop this into your terminal to download and extract the latest release:

```bash
wget https://github.com/BiosSystem/AuraTorrent/releases/latest/download/auratorrent.zip
unzip auratorrent.zip -d /path/to/qbittorrent/webui
```
Then, in qBittorrent: Go to `Options -> WebUI`, check **Use alternative Web UI**, and point it to the `/path/to/qbittorrent/webui` folder.

## 🛠️ Full Developer Setup

To build from source or contribute:

```bash
git clone https://github.com/BiosSystem/AuraTorrent.git
cd AuraTorrent
npm install
npm run dev
```

## 🏛️ Attribution & Credits

AuraTorrent builds upon the extraordinary open-source PWA foundation of **VueTorrent**. We honor and attribute the core architecture to **WDaan** and the VueTorrent contributor community.

- **Original Repository**: [VueTorrent](https://github.com/VueTorrent/VueTorrent)
- **License**: GPL-3.0

---
*Crafted with passion for the Open Source community by BiosSystem.*
