# Bandwidth Scheduler Matrix

The Bandwidth Scheduler Matrix is a flagship feature of AuraTorrent that visually represents and controls the application's global bandwidth limits across a 7-day, 24-hour cycle.

## Core Logic

qBittorrent natively supports an "Alternative Speed Limit" schedule, but its configuration is limited to simple start/end times. AuraTorrent bypasses this limitation by implementing a client-side crontab-like scheduler.

1. **The Grid (7x24)**: The UI presents a 168-cell matrix representing every hour of the week.
2. **Cell States**: Each cell can hold one of three states:
   - `Normal` (Default limits)
   - `Throttled` (Alternative limits)
   - `Unmetered` (Infinite limits)
3. **Tick Evaluation**: A background Vue watcher evaluates the current system time every 60 seconds against the matrix configuration.

## API Execution

When a boundary condition is crossed (e.g., crossing from a `Throttled` hour into a `Normal` hour), the frontend dispatches a REST API call to qBittorrent:

```javascript
// Activating Alternative Limits
POST /api/v2/transfer/toggleSpeedLimitsMode
```

## Resilience and Fallback

If the browser tab is closed, the client-side scheduler cannot execute. Therefore, power users are encouraged to keep the PWA running in the background or rely on the native qBittorrent scheduler as a fallback.
