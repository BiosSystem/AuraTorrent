# AuraTorrent Credits & Acknowledgments

**AuraTorrent** is the enterprise-grade, hardened WebUI skin for qBittorrent, engineered as part of the **BiosSystem** open-source project suite.

---

## 🏛️ Upstream Foundation & Core Authorship

AuraTorrent is a fork of **VueTorrent**, and we explicitly acknowledge, honor, and attribute the upstream architecture of this project to **WDaan** and the entire VueTorrent open-source community.

| Upstream Project | Author / Org | Link |
|---|---|---|
| [VueTorrent](https://github.com/VueTorrent/VueTorrent) | WDaan & VueTorrent Contributors | [MIT License](https://github.com/VueTorrent/VueTorrent/blob/latest-release/LICENSE) |

---

## 🚀 Core Runtime Dependencies

| Library | Author / Org | License |
|---|---|---|
| [Vue 3](https://github.com/vuejs/core) | Evan You & Vue.js Contributors | MIT |
| [Vuetify](https://github.com/vuetifyjs/vuetify) | John Jeremy Leider & Vuetify Contributors | MIT |
| [Vite](https://github.com/vitejs/vite) | Evan You & Vite Contributors | MIT |
| [Pinia](https://github.com/vuejs/pinia) | Eduardo San Martin Morote | MIT |
| [Vue Router](https://github.com/vuejs/router) | Evan You & Vue.js Contributors | MIT |
| [VueUse](https://github.com/vueuse/vueuse) | Anthony Fu & VueUse Contributors | MIT |
| [vue-i18n](https://github.com/intlify/vue-i18n) | Kazuya Kawaguchi (intlify) | MIT |
| [Pixi.js](https://github.com/pixijs/pixijs) | Mat Groves & PixiJS Contributors | MIT |
| [ApexCharts](https://github.com/apexcharts/apexcharts.js) | ApexCharts Contributors | MIT |
| [DOMPurify](https://github.com/cure53/DOMPurify) | Mario Heiderich / cure53 | Apache 2.0 / MPL 2.0 |
| [Day.js](https://github.com/iamkun/dayjs) | iamkun | MIT |
| [Axios](https://github.com/axios/axios) | Matt Zabriskie & Axios Contributors | MIT |
| [vuedraggable](https://github.com/SortableJS/Vue.Draggable) | SortableJS Contributors | MIT |
| [SortableJS](https://github.com/SortableJS/Sortable) | Owen Buckley & SortableJS Contributors | MIT |
| [vue3-toastify](https://github.com/jerrywu001/vue3-toastify) | jerrywu001 | MIT |
| [zip.js](https://github.com/gildas-lormeau/zip.js) | Gildas Lormeau | BSD-3 |
| [pinia-persistence-plugin](https://github.com/bytemind-de/pinia-persistence-plugin) | ByteMind | MIT |
| [vue-concurrency](https://github.com/MartinMalinda/vue-concurrency) | Martin Malinda | MIT |
| [@ctrl/tinycolor](https://github.com/scttcper/tinycolor) | Scott Cooper | MIT |
| [uuid](https://github.com/uuidjs/uuid) | Robert Kieffer & uuid Contributors | MIT |
| [lodash.debounce](https://github.com/lodash/lodash) | John-David Dalton & Lodash Contributors | MIT |
| [@flatten-js/interval-tree](https://github.com/alexbol99/flatten-js) | Alex Bol | MIT |
| [@faker-js/faker](https://github.com/faker-js/faker) | Faker.js Contributors | MIT |

## 🎨 Fonts & Icons

| Resource | Author / Org | License |
|---|---|---|
| [Roboto Font](https://fonts.google.com/specimen/Roboto) | Christian Robertson / Google | Apache 2.0 |
| [Material Design Icons](https://github.com/Templarian/MaterialDesign) | Austin Andrews & MDI Contributors | Apache 2.0 |

## 🛠️ Build & Dev Toolchain

| Tool | Author / Org | License |
|---|---|---|
| [TypeScript](https://github.com/microsoft/TypeScript) | Microsoft | Apache 2.0 |
| [ESLint](https://github.com/eslint/eslint) | ESLint Contributors | MIT |
| [Prettier](https://github.com/prettier/prettier) | Prettier Contributors | MIT |
| [Vitest](https://github.com/vitest-dev/vitest) | Anthony Fu & Vitest Contributors | MIT |
| [Sass](https://github.com/sass/dart-sass) | Google & Sass Contributors | MIT |
| [vite-plugin-pwa](https://github.com/vite-pwa/vite-plugin-pwa) | Anthony Fu | MIT |
| [LightningCSS](https://github.com/parcel-bundler/lightningcss) | Devon Govett / Parcel | MIT |

---

## ⚙️ BiosSystem Hardening & Enhancements

This release was rebranded and enhanced by the **BiosSystem** team with:

1. **AuraTorrent Brand Identity** - Visual and architectural integration with the BiosSystem ecosystem
2. **WebSocket Auto-Reconnect** - Exponential backoff recovery logic for qBittorrent daemon restarts
3. **Physical Directory Alignment** - `auratorrent/public` packaging to resolve qBittorrent C++ web server parsing errors
4. **Multi-Daemon Server Switcher** - Glassmorphic navbar dropdown for managing multiple qBittorrent instances
5. **BiosSystem Easter Eggs** - Diagnostic HUD overlays and B-I-O-S keyboard sequence
6. **Bandwidth Scheduler** - Interactive weekly speed limit timetable backed by Pinia + localStorage
7. **ThemeLab** - Real-time CSS custom property editor for live theme customization
8. **SpeedTicker** - Animated live transfer speed display

---

*Powered by BiosSystem - Open Source Community*
