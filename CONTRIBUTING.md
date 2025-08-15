# Contributing to AuraTorrent

This project accepts contributions from the community. Please read these guidelines before opening a pull request.

## Repository Owner

BiosSystem - https://github.com/BiosSystem

## Attribution

AuraTorrent is a fork of [VueTorrent](https://github.com/VueTorrent/VueTorrent) by WDaan. Please see [CREDITS.md](CREDITS.md) for full upstream attribution.

## Commit Guidelines

- Author identity: `BiosSystem`
- Plain imperative messages: `Add PWA offline support`, `Fix sidebar navigation`, `Update qBittorrent API mapping`
- No `feat:` / `fix:` / `chore:` prefixes in commit subjects
- No AI signatures

## Development Workflow

```bash
npm install

# Dev server
npm run dev

# Type-check
vue-tsc

# Production build
npm run build

# Run post-build packaging
node postbuild.cjs
```

## Scope Policy

AuraTorrent is a frontend dashboard for qBittorrent / seedbox environments. Keep changes focused on:
- UI improvements and accessibility
- qBittorrent API compatibility
- PWA and enterprise NAS performance
- BiosSystem branding (B-I-O-S easter egg, `cdn.jsdelivr.net/gh/BiosSystem` CDN assets)

Do not add backend server components or change the core VueTorrent architecture without discussion.
