# AuraTorrent Architectural Handover

This document strictly tracks architectural deltas from upstream components and key decisions made for the BiosSystem Enterprise environment.

## [1.6.0] Modernization & DX (2026-07-10)

### 1. Command Palette Implementation
*   **Decision**: Implemented a global Command Palette (`Cmd/Ctrl+K`) for power users to navigate quickly.
*   **Security Context**: Instead of pulling in third-party unvetted dependencies like `ninja-keys`, the command palette was built *natively* using Vuetify's `<v-dialog>` and `<v-autocomplete>`. This guarantees 0 added attack surface and 0 bundle bloat while utilizing community-approved components.
*   **Code Location**: `src/components/Core/CommandPalette.vue`, mounted globally in `src/App.vue`.

### 2. Auto-Import Infrastructure
*   **Decision**: Integrated `unplugin-auto-import` into Vite and TypeScript.
*   **Impact**: Future developers do not need to manually `import { ref, computed } from 'vue'` in `.vue` files or composables. 
*   **Safety Strategy**: The existing codebase's manual imports were explicitly *not* stripped via regex, ensuring zero breakage of complex edge-cases and avoiding ESLint conflicts (which currently suffers from a known upstream bug between `eslint@10` and `eslint-plugin-import`).

## [1.5.1] CI/CD Optimization (2026-07-10)
*   **Action**: Pinned `typescript@~6.0.3` to resolve module resolution failures with ESLint/TS 7.
*   **Action**: Removed `esbuild` minifier in favor of Vite 8's native `Rolldown`.
*   **Action**: Consolidated redundant GitHub Actions CI image builds.
