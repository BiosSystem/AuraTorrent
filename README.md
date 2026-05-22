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
  <img src="https://img.shields.io/github/stars/BiosSystem/AuraTorrent?style=flat-square&color=00ff72" alt="Stars">
</p>

---

**AuraTorrent** is a beautiful, lightning-fast open-source WebUI for qBittorrent. Built on Vue 3 and Vite, it reimagines the seedbox experience with dynamic scheduling, real-time telemetry HUDs, and deep customization.

<p align="center">
  <h3>⚡ WebUI Overview & Torrent Dashboard</h3>
  <img src="https://raw.githubusercontent.com/BiosSystem/AuraTorrent/master/docs/screenshots/auratorrent_overview.png" width="800" alt="AuraTorrent Overview" />
</p>

<p align="center">
  <h3>📅 Bandwidth Scheduler Heatmap Matrix</h3>
  <img src="https://raw.githubusercontent.com/BiosSystem/AuraTorrent/master/docs/screenshots/auratorrent_scheduler.png" width="800" alt="Bandwidth Scheduler Heatmap" />
</p>

<p align="center">
  <h3>🎨 ThemeLab CSS customization Engine</h3>
  <img src="https://raw.githubusercontent.com/BiosSystem/AuraTorrent/master/docs/screenshots/auratorrent_themelab.png" width="800" alt="ThemeLab CSS customization" />
</p>

<p align="center">
  <h3>📈 Speed Ticker HUD (Sparkline Speeds overlay)</h3>
  <img src="https://raw.githubusercontent.com/BiosSystem/AuraTorrent/master/docs/screenshots/auratorrent_speedticker.png" width="800" alt="Speed Ticker HUD" />
</p>

<p align="center">
  <h3>🖥️ B-I-O-S Kernel Diagnostic Overlay</h3>
  <img src="https://raw.githubusercontent.com/BiosSystem/AuraTorrent/master/docs/screenshots/auratorrent_easteregg.png" width="800" alt="BiosSystem Kernel Diagnostic Overlay" />
</p>

## ✨ Why It's Unique

Unlike standard qBittorrent WebUIs, AuraTorrent includes next-gen features designed for power users:

- **Bandwidth Scheduling Matrix** — A 7×24 visual heatmap grid to paint your bandwidth schedule visually. The UI automatically throttles qBittorrent based on the current hour.
- **AuraTheme Engine** — A live, built-in CSS variable editor. Adjust glassmorphism blur, neon glow intensity, and accent colors in real-time, then export to JSON.
- **Global Speed Ticker** — Press `Ctrl+Shift+T` anywhere to summon a floating, always-on-top HUD sparkline graph of your current I/O speeds.
- **B-I-O-S Easter Egg** — Type `B-I-O-S` on your keyboard to unlock the BiosSystem Kernel Diagnostic HUD.

## 📊 Feature Matrix Comparison

Here is how **AuraTorrent** stacks up against the competition in the qBittorrent WebUI ecosystem.

| Feature | AuraTorrent | VueTorrent | Flood | Default UI |
|---|:---:|:---:|:---:|:---:|
| **Modern Neon Glassmorphism UI** | ✅ | ❌ | ❌ | ❌ |
| **Mobile Responsive (PWA)** | ✅ | ✅ | ✅ | ❌ |
| **Telegram Companion Bot (AuraBot)**| ✅ | ❌ | ❌ | ❌ |
| **Live Theme Editor Lab** | ✅ | ❌ | ❌ | ❌ |
| **Multi-Daemon Switcher** | ✅ | ❌ | ❌ | ❌ |
| **Visual Bandwidth Heatmap** | ✅ | ❌ | ❌ | ❌ |
| **Global Speed Ticker HUD** | ✅ | ❌ | ❌ | ❌ |

## 🖥️ Platform Support

| Platform | Support | Notes |
|---|:---:|---|
| **Windows / macOS / Linux** | ✅ Native | Works in any modern desktop browser. |
| **iOS / iPadOS** | ✅ PWA | Add to Home Screen for a native app-like experience. |
| **Android** | ✅ PWA | Install via Chrome. Handles `magnet:` links directly. |
| **Docker / Seedboxes** | ✅ Supported | Mount into your container's WebUI folder. |

## 🚀 Quick Start

```bash
wget https://github.com/BiosSystem/AuraTorrent/releases/latest/download/auratorrent.zip
unzip auratorrent.zip -d /path/to/qbittorrent/webui
```

Then in qBittorrent: go to `Options → WebUI`, check **Use alternative Web UI**, and point it to the folder.

## 🛠️ Developer Setup

```bash
git clone https://github.com/BiosSystem/AuraTorrent.git
cd AuraTorrent
npm install
npm run dev
```

## 📖 Documentation

Full documentation is available in the **[Wiki](https://github.com/BiosSystem/AuraTorrent/wiki)**.

## 🙏 Attribution & Credits

AuraTorrent builds upon the open-source PWA foundation of **VueTorrent**. We honor and attribute the core architecture to **WDaan** and the VueTorrent contributor community.

- **Original Repository**: [VueTorrent](https://github.com/VueTorrent/VueTorrent)
- **License**: GPL-3.0

## 🔒 Security Fixes & Information

AuraTorrent is built with safety and code integrity in mind:
- **Zero-Vulnerability Baseline**: Regularly audited dependencies to ensure `npm audit` reports 0 vulnerabilities.
- **Strict WebUI Sandboxing**: Enforces restricted API communications and secure CORS configurations.
- **Upstream Parity Security Fixes**: Integrates upstream patches directly from verified VueTorrent pull requests.

For detailed security policies, reporting guidelines, and contact information, please refer to our [Security Policy](SECURITY.md).

---
*Copyright © 2026 BiosSystem | Powered by BiosSystem Kernel*
