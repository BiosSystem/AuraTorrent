# AuraTorrent Architectural Improvement Plan

This roadmap outlines specific, actionable refactoring steps to elevate AuraTorrent to top-tier enterprise standards. The improvements focus on decoupling architecture, enforcing strict type safety, and improving error resilience—all without modifying the core functionality.

## [x] 1. Implement API Error Interceptors & Retry Mechanisms (Critical / Reliability)

**Problem:** `src/services/backend.ts` manually suppresses API errors, returning boolean flags or `null`. The Python bot uses hardcoded `for attempt in range(2):` loops.
**Action:** 
- Implement global Axios interceptors for the Vue frontend to handle 401/403 responses and trigger automatic token refreshes or logouts.
- Introduce `tenacity` (or robust `aiohttp` retry middleware) in the Python bot to handle network jitter and connection pooling.

**Before (Frontend):**
```typescript
async get(key: string): Promise<string | null> {
  if (!this.up) return null
  return this.axios.get(`/config/${key}`).then(
    res => res.data[key],
    () => null // Error swallowed
  )
}
```

**Target (Frontend):**
```typescript
async get(key: string): Promise<string> {
  // Axios interceptor handles global errors; this throws properly if failed.
  const response = await this.axios.get<{ [key: string]: string }>(`/config/${key}`)
  return response.data[key]
}
```

## 2. Decouple Pinia State Management (High / Architecture) [COMPLETED]

**Problem:** `src/stores/maindata.ts` acts as a monolithic controller, manually invoking sync methods on 5 different stores. This tight coupling makes unit testing difficult and breaks modularity.
**Action:** 
- Converted `maindataStore` to expose `rawPayload` which child stores subscribe to via `watch()`.
- Used strict typed `try/catch (error: unknown)` error boundaries with `isAxiosError` instead of `catch (error: any)`.

**Before:**
```typescript
// Inside updateMaindata()
if (isFullUpdate(response)) {
  syncFromMaindata(true, response.server_state)
  categoryStore.syncFromMaindata(true, Object.entries(response.categories ?? {}))
  tagStore.syncFromMaindata(true, response.tags ?? [])
  torrentStore.syncFromMaindata(true, Object.entries(response.torrents ?? {}))
  trackerStore.syncFromMaindata(true, Object.entries(response.trackers ?? {}))
  return
}
```

**Target:**
```typescript
// Inside maindata.ts - purely updates its own state
if (isFullUpdate(response)) {
  this.serverState = response.server_state
  this.rawPayload = response // Other stores react to this payload changing
  return
}

// In categoryStore.ts (Decoupled Subscription)
maindataStore.$subscribe((mutation, state) => {
  if (state.rawPayload?.categories) {
    this.syncFromMaindata(state.rawPayload.categories)
  }
})
```

## 3. Formalize Python Bot State Machine (Medium / Maintainability) [COMPLETED]

**Problem:** `bot/main.py` uses nested `if/elif` statements and raw strings to manage torrent state transitions, making it fragile and difficult to extend.
**Action:** 
- Introduced a strict `Enum` for `TorrentState` with a robust fallback to `UNKNOWN` using `_missing_`.
- Decoupled state transition formatting logic into `handle_transition()`.

**Before:**
```python
if t_hash in known_torrents:
    prev_state = known_torrents[t_hash]
    if prev_state != state:
        if state == "uploading" and prev_state == "downloading":
            await broadcast_message(_fmt_finished(name))
        elif state in ("error", "missingFiles"):
            await broadcast_message(_fmt_error(name, state))
```

**Target:**
```python
from enum import Enum

class TorrentState(str, Enum):
    DOWNLOADING = "downloading"
    UPLOADING = "uploading"
    ERROR = "error"
    MISSING_FILES = "missingFiles"

def handle_transition(prev: TorrentState, new: TorrentState, name: str):
    if prev == TorrentState.DOWNLOADING and new == TorrentState.UPLOADING:
        return _fmt_finished(name)
    if new in (TorrentState.ERROR, TorrentState.MISSING_FILES):
        return _fmt_error(name, new.value)
    return None
```

## 4. Enforce Strict Typing in Python (Low / DX & Linting) [COMPLETED]

**Problem:** Standard dictionaries and lists are used without `TypedDict` or `dataclasses`, limiting IDE autocomplete and allowing runtime schema errors.
**Action:** 
- Replaced generic `dict`/`list` annotations with `TypedDict` (`TorrentData`) for the API responses.

**Before:**
```python
known_torrents: dict = {}

def get_torrents(self) -> Optional[list]:
    # Returns raw JSON list
```

**Target:**
```python
from typing import Dict, List, Optional
from pydantic import BaseModel

class TorrentData(BaseModel):
    hash: str
    name: str
    state: TorrentState

known_torrents: Dict[str, TorrentState] = {}

async def get_torrents(self) -> Optional[List[TorrentData]]:
    # Validate and return strongly typed models
```
