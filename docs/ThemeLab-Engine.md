# ThemeLab Engine

The ThemeLab Engine is AuraTorrent's dynamic CSS customization framework. It allows users to modify the visual appearance of the application in real-time, tweaking everything from neon glow intensities to background blur radii.

## How It Works

ThemeLab operates entirely at runtime by manipulating CSS Custom Properties (Variables) attached to the `:root` element. 

### State Persistence

1. **Reactive Store**: The `ThemeStore` (Pinia) holds a reactive object representing all customizable properties (e.g., `--primary-color`, `--glass-blur`).
2. **IndexedDB Backup**: Because `localStorage` is synchronous and can block the main thread, ThemeLab persists the active theme configuration asynchronously to `IndexedDB` using the localforage library.
3. **DOM Injection**: A Vue watcher observes the `ThemeStore` and dynamically updates the `document.documentElement.style` properties whenever a value changes.

## Glassmorphism

AuraTorrent heavily utilizes the `backdrop-filter` CSS property to achieve its signature glassmorphism look. The ThemeLab engine allows tuning of:
- `backdrop-filter: blur(Xpx)`
- `background-color: rgba(X, X, X, Y)` (Opacity control)

This ensures the UI can adapt to visually busy wallpapers without compromising text readability.

## Exporting Themes

Themes can be exported as JSON payloads. This simply serializes the `ThemeStore` state object into a string, allowing users to share their creations or back them up.
