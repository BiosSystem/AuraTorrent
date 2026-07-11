# Security Policy & Hardening (AuraTorrent)

Security is a primary focus of the AuraTorrent project. Since forking from the upstream `WDaan/VueTorrent` codebase, the BiosSystem community has performed comprehensive vulnerability audits and refactored multiple core files to eliminate serious security risks and establish a hardened WebUI posture.

This document outlines our security architecture, details the complete security patches history since the VueTorrent fork, and provides best practices for secure deployment.

---

## Supported Versions

Only the active release branch and tags under the BiosSystem namespace are supported with security updates.

| Version | Supported |
| ------- | --------- |
| >= 1.3  | ✅ Yes    |
| < 1.3   | ❌ No     |

---

## Reporting a Vulnerability

If you discover a security vulnerability in AuraTorrent or its companion bot, please report it immediately. To protect the seedboxes and environments of our users, **do not open a public issue on GitHub**.

* **Email**: Send detailed vulnerability reports to `security@bios-system.net`.
* **Response SLA**:
  * **Acknowledgement**: Within 24 hours.
  * **Remediation Plan**: Within 3 business days.
  * **Disclosure**: Coordinated with the reporter after patches are deployed and verified.

---

## Security Architecture & Hardening History (Since VueTorrent Fork)

Below is an in-depth breakdown of the security refactoring and vulnerability patches implemented in AuraTorrent compared to the original upstream VueTorrent codebase:

### 1. Phishing & Open Redirect Patch
* **Target File**: `src/pages/Login.vue`
* **Vulnerability & Threat Vector**:
  In original VueTorrent implementations, the application extracted the `redirect` URL parameter from the route query string and passed it directly to the router push method (`void router.push(route.query.redirect as string)`) upon successful authentication. Because this value was not validated, attackers could construct phishing campaigns by distributing links like:
  `http://<seedbox-ip>:<port>/#/login?redirect=https://evil-harvesting-site.com`
  A user clicking the link would see a legitimate login page, enter their credentials, and be redirected to the external site, potentially leaking session cookies or being tricked by a cloned interface.
* **Remediation**:
  Refactored the `redirectOnSuccess` handler in `src/pages/Login.vue` to strictly validate the destination URL. It checks if the redirect target is a relative path (starting with a single `/`) and explicitly rejects protocol-relative paths (starting with `//`). If the target is absolute or invalid, the handler falls back safely to the internal dashboard.
* **Code Modification**:
  ```diff
  -  if (route.query.redirect) {
  -    void router.push(route.query.redirect as string)
  +  const redirect = route.query.redirect as string | undefined
  +  if (redirect && redirect.startsWith('/') && !redirect.startsWith('//')) {
  +    void router.push(redirect)
     } else {
       void router.push({ name: 'dashboard' })
     }
  ```

### 2. URL Credential Leakage Prevention
* **Target File**: `src/pages/Login.vue`
* **Vulnerability & Threat Vector**:
  Upstream VueTorrent contained an automatic login hook on mount. If the query parameters `username` and `password` were present in the URL, the page automatically called the login API. 
  Passing credentials in the query string (e.g., `?username=admin&password=adminadmin`) is a severe security risk:
  1. Plaintext credentials are saved in the browser's history database.
  2. Intermediate proxy servers, firewalls, and reverse proxies record the entire URL, including query parameters, in their plaintext access logs.
  3. External assets or outgoing links can leak the query string to third parties via the HTTP `Referer` header.
* **Remediation**:
  Removed the query parameter extraction block from the `onMounted` hook completely. Credentials must now be entered through the secure form input fields and submitted only in the request body of POST requests.
* **Code Modification**:
  ```diff
  -onMounted(async () => {
  -  if (route.query.username && route.query.password) {
  -    await appStore.login(route.query.username as string, route.query.password as string)
  -  }
  +onMounted(() => {
  +  // Auto-login via URL query params was removed to prevent credential exposure in logs and history
   })
  ```

### 3. Local Storage Brand & Namespace Isolation
* **Target Files**: `src/components/Dialogs/ImportSettingsDialog.vue`, `src/components/Settings/VueTorrent/General.vue`
* **Design Defect**:
  The upstream application stored its settings state in `localStorage` under the key `vuetorrent_webuiSettings`. When hosting multiple forks or instances of WebUI clients on the same host and port (e.g. sharing a reverse proxy domain or localhost testing), the configurations clashed, resulting in settings pollution, corruption, or cross-client preference hijacking.
* **Remediation**:
  Migrated all settings retrieval and persistence handlers to use an isolated namespace: `webuiSettings`. This ensures that AuraTorrent maintains a strict state boundary partition and cannot be influenced by other VueTorrent settings sharing the browser storage origin.
* **Code Modification**:
  ```diff
  -localStorage.setItem('vuetorrent_webuiSettings', settings.value)
  +localStorage.setItem('webuiSettings', settings.value)
  ```

### 4. Telegram Companion Bot Access Controls (AuraBot)
* **Target File**: `bot/main.py`
* **Vulnerability & Threat Vector**:
  The AuraTorrent Telegram bot allows remote monitoring and management of the qBittorrent daemon. If command handlers are left unguarded, any Telegram user who discovers the bot's username can query seedbox statistics, trigger actions, or register themselves as users.
* **Remediation**:
  Implemented an access control verification routine (`is_allowed()`) that checks user IDs against a strict whitelist defined in the `ALLOWED_USERS` environment variable. All command handlers are wrapped in this verification check. Additionally, administrative commands such as `/add_user` are restricted exclusively to the primary owner (`ALLOWED_USERS[0]`), preventing unauthorized users from registering other accounts.
* **Code Implementation**:
  ```python
  def is_allowed(user_id: int) -> bool:
      return not ALLOWED_USERS or user_id in ALLOWED_USERS

  @dp.message(Command("add_user"))
  async def cmd_add_user(message: Message):
      if len(ALLOWED_USERS) > 0 and message.from_user.id != ALLOWED_USERS[0]:
          await message.reply("⛔ Only the primary owner can add users.")
          return
      # ... add user logic
  ```

### 5. Dependency Hardening & 0-Vulnerability Target
* **Target File**: `package-lock.json`
* **Vulnerability & Threat Vector**:
  Original dependencies had vulnerability trails, such as prototype pollution in utility libraries and cross-site scripting vulnerabilities in third-party cookie handlers.
* **Remediation**:
  Performed multiple audit runs and upgraded packages to their secure baselines. For example, `js-cookie` was upgraded from `3.0.5` to `3.0.7` to prevent prototype pollution vectors. The project is maintained at a strict target of `0` vulnerabilities on npm audits.

### 6. Content Security Policy and Response Header Hardening (v1.7.0)
* **Target File**: `nginx.conf`, `Dockerfile`
* **Vulnerability & Threat Vector**:
  The published container image served the built assets with nginx's bare defaults: no `Content-Security-Policy`, no `X-Frame-Options`, no `X-Content-Type-Options`. A stored or reflected XSS anywhere in the SPA (torrent names, tracker URLs, RSS content) had no browser-side containment, and the WebUI could be framed by a third-party origin for clickjacking.
* **Remediation**:
  Added a dedicated `nginx.conf` served by the container's `serve` stage, restricting script and connection origins to `'self'`, disabling framing from other origins, and setting `X-Content-Type-Options: nosniff` and a restrictive `Permissions-Policy`. `worker-src` and `manifest-src` are explicitly allowed for `'self'` so the PWA service worker and manifest keep working under the policy.
* **Deployment Note**:
  If `VITE_QBITTORRENT_TARGET` points at a different origin than the one serving the UI, `connect-src` in `nginx.conf` must be widened to include it, or requests will be blocked by the browser.

### 7. Telegram Bot Rate Limiting and Unauthorized Access Alerting (v1.7.0)
* **Target File**: `bot/main.py`
* **Vulnerability & Threat Vector**:
  Command handlers had no rate limit. A user with a valid Telegram account, allowed or not, could send commands in a tight loop, driving repeated calls against the qBittorrent API or flooding application logs with rejected-access entries with no operator visibility.
* **Remediation**:
  Added a per-user sliding-window rate limiter (`RATE_LIMIT_MAX` commands per `RATE_LIMIT_WINDOW` seconds, default 5 per 10) applied to every command handler through a `guarded` decorator. Unauthorized attempts are now logged with the user id and username and trigger a throttled Telegram alert to the bot owner (`UNAUTHORIZED_ALERT_COOLDOWN`, default 300 seconds, prevents alert flooding from a persistent attacker). `/start` no longer confirms the bot's identity to unauthorized users, removing an enumeration signal.

### 8. Supply Chain Integrity (v1.7.0)
* **Target Files**: `.github/workflows/*.yml`
* **Vulnerability & Threat Vector**:
  Workflows referenced third-party GitHub Actions by mutable version tags (e.g. `@v6`) and one by a mutable branch (`@main`). A compromised upstream action repository could push malicious code to that tag or branch and have it run in CI with `packages: write` and `contents: write` permissions without any change to this repository.
* **Remediation**:
  All actions across every workflow are now pinned to a specific commit SHA, with the original version kept as a trailing comment for readability. Added `actions/dependency-review-action` as a required PR check that fails on high-severity vulnerable or newly disallowed dependencies. The published container image is now signed keylessly with `cosign` and accompanied by an SPDX SBOM (`anchore/sbom-action`), attested to the image digest, so the image's provenance and contents can be verified with `cosign verify`.

---

## Secure Deployment Guidelines

To maintain the security boundaries established in the code, users must follow these deployment recommendations:

1. **Enable HTTPS**: Always serve AuraTorrent over TLS/SSL. Use a reverse proxy (e.g., Nginx, Caddy, or Traefik) to terminate SSL connections.
2. **Enable CSRF Protection**: Ensure that qBittorrent CSRF protection is active under `Options -> WebUI -> Enable Cross-Site Request Forgery (CSRF) protection`.
3. **Restrict Host Access**: In `vite.config.ts` during development, do not expose the server to the entire LAN (`0.0.0.0`) unless absolutely necessary. The default configuration restricts development bindings to `127.0.0.1`.
4. **Secure reverse proxy headers**: Configure proxy rules to avoid trusting arbitary `X-Forwarded-For` headers from clients by disabling `xfwd` options, enforcing local header override setups.
