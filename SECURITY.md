# Security Policy

## Supported Versions

The following versions of AuraTorrent are currently supported with security updates:

| Version | Supported |
| ------- | --------- |
| >= 1.3  | ✅ Yes    |
| < 1.3   | ❌ No     |

## Reporting a Vulnerability

If you discover a security vulnerability in AuraTorrent, please report it immediately. Do not open a public issue on GitHub.

*   **Email**: Send reports to `security@bios_system.io`
*   **PGP Key**: (Optional) Encrypt your report using the PGP key associated with `security@bios_system.io`.
*   **Response Time**: We acknowledge receipt of reports within 24 hours and aim to provide a remediation plan within 3 business days.

---

## Security Fixes History (Since VueTorrent Fork)

Since forking from VueTorrent, the BiosSystem core team has performed comprehensive security audits and implemented key defensive remediations to ensure a hardened WebUI posture:

### 1. Phishing & Open Redirect Patch (Login.vue)
* **Vulnerability**: The previous `redirect` mechanism accepted absolute and protocol-relative URLs (`//evil.com`), allowing attackers to construct login links that redirect users to credential-harvesting sites upon successful authentication.
* **Remediation**: Refactored the `redirectOnSuccess` handler in `Login.vue` to strictly check and validate the destination URL:
  * Only relative paths starting with a single `/` are allowed.
  * Paths starting with `//` (protocol-relative) are rejected.
  * Falls back securely to the internal dashboard.

### 2. URL Credential Leakage Prevention (Login.vue)
* **Vulnerability**: Support for automatic login via query parameters (e.g. `?username=admin&password=secret`) leaked highly sensitive cleartext credentials. These parameters were written to the browser history database, proxy caches, and server logs.
* **Remediation**: Removed automatic query parameter extraction on mount, forcing login parameters through standard, secure POST/request body flows only.

### 3. Client-Side Storage Brand Isolation (Settings Import/Export)
* **Design Issue**: Using the upstream `vuetorrent_webuiSettings` localStorage namespace exposed settings to conflicts and cross-app tampering if multiple WebUI variants shared the same local domain/port.
* **Remediation**: Rebuilt Settings logic to utilize the isolated namespace `webuiSettings`, partitioning the application state from other VueTorrent-derived instances.

### 4. Dependency Hardening & 0-Vulnerability Target
* **Vulnerability**: Multi-layered JS dependency chains contained known high-severity vulnerabilities (e.g. CVEs in utility packages).
* **Remediation**: Updated key dependencies (including updating `js-cookie` from `3.0.5` to `3.0.7`) and locked versions to maintain a strict `npm audit` report of zero vulnerabilities.

### 5. Telegram Companion Bot Access Controls (AuraBot Authentication)
* **Vulnerability**: Unauthenticated control of seedboxes via Telegram bots can lead to remote arbitrary downloads, deletion of content, or data exposure if any user on Telegram can message the bot.
* **Remediation**: Implemented the `ALLOWED_USERS` strict whitelist check at the dispatcher level for all commands (`/start`, `/status`, `/add_user`). Restricts administrative operations (like `/add_user`) exclusively to the primary owner (`ALLOWED_USERS[0]`), preventing unauthorized control of the seedbox daemon.


