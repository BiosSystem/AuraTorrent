# AuraTorrent Architectural Handover

This document strictly tracks architectural deltas from upstream components and key decisions made for the BiosSystem Enterprise environment.

## [1.7.0] Security Hardening and Supply Chain Integrity (2026-07-11)

### 1. Response Header Hardening
*   **Decision**: Added a dedicated `nginx.conf`, served by the container's `serve` stage, setting a Content-Security-Policy plus `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`.
*   **Security Context**: Upstream and prior AuraTorrent images relied on nginx's bare defaults. `connect-src`, `script-src`, and `frame-ancestors` are scoped to `'self'`, containing any future XSS and preventing clickjacking. `worker-src`/`manifest-src` are explicitly allowed so the PWA service worker keeps functioning.
*   **Code Location**: `nginx.conf`, `Dockerfile`.

### 2. Telegram Bot Rate Limiting and Alerting
*   **Decision**: Added a per-user sliding-window rate limiter and owner alerting on unauthorized access, wired through a `guarded` decorator around every command handler.
*   **Security Context**: Closes a gap where an allowed or unauthorized user could hammer the bot with commands with no cost and no operator visibility into repeated unauthorized attempts.
*   **Code Location**: `bot/main.py` (`is_rate_limited`, `guarded`, `_alert_owner_unauthorized`).

### 3. Release Pipeline Retirement of release-please
*   **Decision**: Retired `release-please` in favor of a tag-driven release workflow.
*   **Reasoning**: `release-please` requires conventional-commit prefixes (`feat:`, `fix:`, `chore:`) to detect what to release, which conflicts directly with this project's commit guidelines (see `CONTRIBUTING.md`). The new flow: bump `package.json` and `CHANGELOG.md`, push a `vX.Y.Z` tag, CI builds the release from the tag.
*   **Code Location**: `.github/workflows/build-release.yml`, `CONTRIBUTING.md`.

### 4. Supply Chain Integrity
*   **Decision**: Pinned every third-party GitHub Action, across all workflows, to a commit SHA (version kept as a trailing comment). Added `actions/dependency-review-action` as a required PR gate. Added SBOM generation (`anchore/sbom-action`) and keyless image signing (`cosign`) to the container publish job.
*   **Security Context**: A mutable tag or branch reference (`@v6`, `@main`) lets a compromised upstream action run arbitrary code in CI with write permissions to this repository and its packages, with no diff on our side to review. Pinning to a SHA closes that gap. Signing and the SBOM let anyone verify the published image's provenance and contents with `cosign verify`.
*   **Code Location**: `.github/workflows/*.yml`.

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
