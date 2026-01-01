<p align="center">
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/AuraTorrent-logo.png" width="300" alt="AuraTorrent Logo" />
</p>

# AuraTorrent

A beautiful, lightning-fast Open Source WebUI for qBittorrent, crafted with passion by **Bios System**.

[![Discord](https://img.shields.io/discord/1170618192956243998?logo=discord)](https://discord.gg/KDQP7fR467)
![Vue](https://img.shields.io/badge/Vue-%5E3.4.26-brightgreen) ![Vuetify](https://img.shields.io/badge/Vuetify-%5E3.6.4-brightgreen)
![qBittorrent](https://img.shields.io/badge/qBittorrent-4.4%2B-brightgreen)
![Version](https://img.shields.io/github/v/release/BiosSystem/AuraTorrent)

---

## ⚡ Passionate Open Source Architecture

**AuraTorrent** takes the extraordinary PWA foundation of upstream WebUIs and reimagines it into a vibrant, ultra-modern experience designed for seedbox enthusiasts and the open-source torrenting community. Built purely out of love for the craft, AuraTorrent focuses on blazing speed, rich aesthetics, and uncompromising community features.

### Key Community Features & Easter Eggs:
1. **WebSocket Auto-Recovery**: Smooth exponential backoff auto-reconnect logic keeps your dashboard alive during qBittorrent daemon restarts or network drops.
2. **Physical Directory Alignment**: Native `auratorrent/public` packaging permanently resolves qBittorrent C++ web server `"Unacceptable file type"` parsing errors.
3. **The B-I-O-S Easter Egg**: Type `B-I-O-S` on your keyboard at any time to unlock BiosSystem's custom real-time diagnostic HUD overlay!
4. **Pure Custom Branding**: 100% independent, community-driven design featuring vibrant electric cyan accents, sleek glassmorphism, and premium dark modes without relying on proprietary corporate trademarks.

---

## 📸 Screenshots

### Desktop (Dark Mode - Aura Obsidian Default)
<p>
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/docs/screenshots/screenshot-desktop-dark-mode.png" width="800" alt="Screenshot Desktop (Dark Mode)" />
</p>

### Desktop (Light Mode - Aura Frost White)
<p>
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/docs/screenshots/screenshot-desktop.png" width="800" alt="Screenshot Desktop (Light Mode)" />
</p>

### Mobile PWA (Dark Mode)
<p>
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/docs/screenshots/screenshot-mobile-dark-mode.png" width="400" alt="Screenshot Mobile Dashboard (Dark Mode)" />
  <img src="https://cdn.jsdelivr.net/gh/BiosSystem/AuraTorrent@master/docs/screenshots/screenshot-mobile-navbar-dark-mode.png" width="400" alt="Screenshot Mobile Navbar (Dark Mode)" /> 
</p>

---

## 🛠️ Installation & Deployment

### 1. Standard qBittorrent WebUI Drop-in
1. Download `auratorrent.zip` from the [Latest Release](https://github.com/BiosSystem/AuraTorrent/releases/latest).
2. Unpack the archive to a local folder (e.g., `/auratorrent`).
3. In qBittorrent: Go to `Options -> WebUI`.
4. Check **Use alternative Web UI** and point the file path to your unpacked `/auratorrent` folder.

### 2. Local Development
```bash
git clone https://github.com/BiosSystem/AuraTorrent.git
cd AuraTorrent
npm install
npm run dev
```

---

## 🏛️ Upstream Credits & Attribution

**AuraTorrent** is built upon the extraordinary open-source foundation of **VueTorrent**. We explicitly acknowledge, honor, and attribute the core PWA architecture to **WDaan** and the upstream VueTorrent contributor community.

*   **Original Upstream Repository**: [VueTorrent on GitHub](https://github.com/VueTorrent/VueTorrent)
*   **Core Upstream Architect**: WDaan & VueTorrent Contributors
*   **License**: Copyright (c) VueTorrent Contributors (GPL-3.0)

---
*Crafted with passion for the Open Source community by BiosSystem.*
