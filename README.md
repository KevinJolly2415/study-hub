# SFIT 5th Sem - Smart Slide Hub 🎓

A lightning-fast, uncluttered local web application for studying SFIT 5th Semester course materials without jitter, lag, or PDF viewer roughness.

---

## 🚀 Quick Start

### 1. Start Development Server
```powershell
cd "C:\Users\kevin\.gemini\antigravity\scratch\study-slides-hub"
npm run dev
```
Runs on `http://localhost:3000`.

### 2. Build Production Bundle
```powershell
npm run build
npm run preview
```

---

## 🌟 Key Features

### 1. 🖥️ Fullscreen Mode (Pure, Distraction-Free Slides)
- Press **`F`** to enter Fullscreen.
- The sidebar and normal navigation completely disappear.
- **MS Edge-Style Auto-Hide Top Bar**:
  - Automatically hides so only the pure slides are on screen.
  - Gently slides down when moving mouse to the top of the screen.
  - Pin button (📌) to lock it visible if you prefer.
- Press **`Esc`** to exit Fullscreen.

### 2. ⚡ Zero-Jitter Instant Slide Jump (`Ctrl + Q`)
- Press **`Ctrl + Q`** to open the quick-jump dialog.
- Type any slide number (e.g. `17`) and press **`Enter`** to land instantly on that slide with zero intermediate jitter or lag.

### 3. 🔍 Find Words in Document (`Ctrl + F`)
- Press **`Ctrl + F`** to open the in-document find bar.
- Highlights matching slides with match counter (`1 of 5`), Next (`Enter` / `↓`), and Previous (`Shift + Enter` / `↑`).

### 4. 📝 Direct Text Selection on All Slides
- Drag your mouse across any text on any slide to highlight and copy (`Ctrl + C`).
- Works on both PDFs and converted PowerPoint decks.

### 5. 🎯 Two Clean View Modes
- **Continuous Mode** (default): Silky-smooth vertical continuous reading feed.
- **Grid Mode**: Bird's-eye overview of all slides in the deck.

### 6. 💾 100% Session & Progress Persistence
- Remembers your exact slide number specifically for each deck.
- Remembers your zoom level, view mode, bookmarks, and whether you were in fullscreen even after sleep or closing the browser.

---

## ⌨️ Keyboard Shortcuts
| Key | Action |
| --- | --- |
| `F` | Toggle Fullscreen Reader |
| `Ctrl + Q` | Jump to Slide Number |
| `Ctrl + F` | Find Words in Document |
| `Ctrl + K` | Global Subject & Slide Search |
| `Ctrl +` / `Ctrl -` | Zoom In / Out |
| `Ctrl 0` | Reset Zoom to 100% |
| `Esc` | Close Search / Dialogs / Exit Fullscreen |
