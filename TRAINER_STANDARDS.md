# Kubi Kids School — Trainer Architecture & UI/UX Standards

This document specifies the standard architecture, user experience, and technical patterns shared across all Kubi educational practice trainers (e.g., **Math Trainer**, **Wortarten Trainer**, **I/Y Trainer**, and **Division with Remainder**). 

Future trainers and existing application refactors should strictly adhere to these specifications to guarantee visual consistency, predictable behavior, and accurate learning analytics.

---

## 1. Core Philosophy & UX Principles

1. **Zero-Scroll Single-Screen View**: The entire practice workspace (matrix, stage, analytics) fits comfortably on standard desktop and tablet viewports without vertical scrolling.
2. **Frictionless Interaction**: Fast keyboard input (1/2/3, Numpad, Enter, Space) and touch-friendly tap targets.
3. **Immediate Positive Feedback**: Correct responses immediately pop with audio and visual feedback; errors give gentle shake animations without punishing the student.
4. **Snappy Transitions**: Fast auto-advance (400ms–500ms) upon finishing a problem or sentence.
5. **Accurate Speed Analytics**: Response times exclude idle or paused time, with an auto-pause at 20 seconds to prevent skewed outlier data.

---

## 2. Standard 3-Column Dashboard Grid

All trainers utilize a CSS Grid layout with three distinct panels:

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: 280px minmax(380px, 1fr) 300px;
  gap: 12px;
  align-items: stretch;
}
```

```
┌─────────────────────────┬───────────────────────────────┬─────────────────────────┐
│       LEFT COLUMN       │         CENTER COLUMN         │      RIGHT COLUMN       │
│      (Matrix Panel)     │         (Stage Panel)         │    (Analytics Panel)    │
│                         │                               │                         │
│ • Title & Progress (M/N)│ • Header & Instructions       │ • Response Time Canvas  │
│ • Mastery Grid (1D/2D)  │ • Problem / Sentence Box      │ • 3-Card KPI Metrics    │
│ • Micro-Legend Swatches │ • Type / Answer Controls      │ • Breakdowns / Tricky   │
│ • Hover Preview Info    │ • Live Scoreboard / Banner    │ • 📅 Daily History (▼)  │
│                         │ • Navigation (Prev/Pause/Next)│   └── 🧹 Reset Button   │
└─────────────────────────┴───────────────────────────────┴─────────────────────────┘
```

### 2.1. Left Column: Mastery Matrix (`.matrix-panel`)
- **Title**: `📊 <Topic> Matrix` with real-time mastery counter (`0/N`).
- **Interactive Grid**: Visual representation of all units (multiplication facts, spelling words, sentences).
  - Unpracticed: Neutral muted border (`var(--border-subtle)`).
  - Mastered (levels 1–6 or 1–3): Teal/Green progression shades.
  - Mistakes: Coral/Red progression shades reflecting remaining mistake countdown.
  - Active Target: Pulsing highlight ring (`active-target`).
- **Micro-Legend**: Compact color legend swatches.
- **Hover Preview (`#hovered-*-info`)**: Shows item text, mastery count, and error history on mouse hover or touch focus.

### 2.2. Center Column: Problem Stage (`.center-panel`)
- **Relative Positioning**: Container has `position: relative;` to host the `#pauseOverlay`.
- **Primary Stage Box**: Large, clear font (e.g. `1.35rem–2.5rem`) with high contrast.
  - Words/Numbers enclosed in distinct bounding boxes (`.word-target`, `.word-active`, `.word-error`).
- **Input Controls**:
  - Direct typing for math (auto-advancing numeric input).
  - Discrete category buttons with numeric badges (`1`, `2`, `3`) for classification.
- **Scoreboard**: Satz/Problem index, Level, Richtig, Falsch, Sterne.
- **Stage Navigation (`.sentence-nav` / `.controls-row`)**:
  - `⬅️ Zurück` (Previous item / undo stack).
  - `⏸ Pause` / `▶️ Weiter` (Toggles pause state).
  - `➡️ Weiter` (Next item / forward stack).
  *(Note: Reset button is NEVER placed between navigation buttons in the center column).*

### 2.3. Right Column: Analytics & History (`.right-analytics-panel`)
- **Title & Sparkline Header**: `📈 Response Time (s)` with optional 80th-percentile badge (`p80Badge`).
- **Response Time Sparkline (`<canvas id="speedChart">`)**: Real-time canvas chart showing recent item response times, a dashed P80 reference line, and outlier markers.
- **3-Card Metric Summary Grid**:
  - Total items solved (`statTotalWords` / `statTotalProblems`).
  - Accuracy percentage (`statWordAccuracy` / `statAccuracy`).
  - Average response time (`statAvgSpeed` / `statAvgTime`).
- **Breakdown / Mistake List**: Topic distribution and tricky item tracking.
- **Collapsible Daily History (`<details>`)**:
  - Placed at the very bottom with `margin-top: auto;`.
  - Summary: `📅 Daily History` (`📅 Tägliche Historie` / `📅 Denná história`).
  - Body: Date-based log lines: `📅 YYYY-MM-DD — N solved | Accuracy% | AvgSpeed s`.
  - **Reset Button**: Positioned inside the details drawer at the bottom right:
    ```html
    <button type="button" class="preset-btn reset-btn" onclick="resetAll()">
      🧹 Reset
    </button>
    ```

---

## 3. Timing, Auto-Pause & Outlier Mitigation

To maintain high data integrity for the speed sparkline and adaptive learning algorithms:

```javascript
let pauseTimeoutSec = 20; // Configurable in settings (default: 20s)
let inactivityRemainingSec = pauseTimeoutSec;
let countdownInterval = null;
let isPaused = false;
let pauseStart = 0;
let totalPausedTime = 0;
let wasCurrentWordPaused = false; // Flag to exclude paused items from speed metrics
```

### 3.1. Inactivity Timeout & Visual Countdown
1. **User Interaction**: Any user interaction (`pointerdown`, `keydown`, input change, choice click) resets the countdown via `resetInactivityTimer()`.
2. **Visual Countdown**: The scoreboard and navigation pause button display the live remaining seconds (e.g. `⏳ Pause in: 20s`, `⏸ Pause (20s)`). When time falls under 5s, the indicator highlights in warning red.
3. **Configurable in Settings**: The top toolbar includes an input allowing students/teachers to adjust the auto-pause duration (5s to 60s, saved to `<app>_pause_timeout` in `localStorage`).
4. **Auto-Pause Trigger**: If the countdown reaches 0, `pauseGame()` / `pauseTrainer()` triggers automatically:
   - Sets `wasCurrentWordPaused = true`.
   - Centers the blurred pause overlay (`#pauseOverlay`).
   - Clicking anywhere or pressing any key resumes the session via `resumeGame()`.

### 3.2. Outlier Prevention: Excluding Paused Items from Speed Chart
To prevent idle time, distraction, or paused states from skewing the student's speed sparkline chart:
1. **Flagging**: When a pause occurs (manually or via timeout), `wasCurrentWordPaused = true` is set.
2. **Exclusion from Antwortzeit**: When the paused word or problem is eventually answered, its time is **NOT** added to `recentWordTimes` / speed sparkline history:
   ```javascript
   if (!wasCurrentWordPaused) {
     recentWordTimes.push(elapsed);
     if (recentWordTimes.length > 30) recentWordTimes.shift();
   } else {
     showMessage("Richtig! 🎉 (Pause: Zeit nicht gewertet ⏱️)");
   }
   ```
3. **Deducting Paused Time**: If a student pauses and resumes, `totalPausedTime` is subtracted from elapsed time:
   ```javascript
   const elapsed = Math.max(0.3, Math.min(pauseTimeoutSec, (performance.now() - startTime - totalPausedTime) / 1000));
   ```
4. **Tab Backgrounding**: Backgrounding the browser tab is tracked via `document.addEventListener("visibilitychange")` and added to `totalPausedTime`.

---

## 4. Smart Progression & Transitions

### 4.1. Auto-Advance Delay
- **Math / Fact Trainers**: `400ms` delay after typing the correct answer.
- **Sentence / Wordart Trainers**: `500ms` delay after completing the final word in a sentence (allowing the kid to enjoy the full sentence colored and the star counter increase).

### 4.2. Timer Guarding
All auto-advancing logic must store its timeout ID:
```javascript
let autoAdvanceTimer = null;

if (autoAdvanceTimer) clearTimeout(autoAdvanceTimer);
autoAdvanceTimer = setTimeout(() => {
  autoAdvanceTimer = null;
  nextItem();
}, 500);
```
- If the user clicks `Weiter ➡️`, switches difficulty presets, clicks a matrix cell, or resets progress while auto-advance is pending, `clearTimeout(autoAdvanceTimer)` is called immediately to prevent accidental double-skips.

### 4.3. Boundary Loop-Around
Reaching the end of a preset list (`currentIndex === maxIndex`) must gracefully loop back to `minIndex`:
```javascript
if (currentIndex < range.max) {
  currentIndex++;
} else {
  showMessage("Stufe gemeistert! 🎉 Von vorne!");
  currentIndex = range.min;
}
```

---

## 5. LocalStorage Data Schema

Trainer data must be partitioned under clear, consistent local storage keys:

| Key Pattern | Description | Structure |
| :--- | :--- | :--- |
| `<app>_progress` | Primary session counters | `{ index: 0, correct: 0, wrong: 0, stars: 0 }` |
| `<app>_matrix` | Mastery states per item | `{ [key]: { completed: 1, mistakes: 0 } }` |
| `<app>_recent_times` | Last 30–50 response times | `[ 1.25, 0.94, 2.10, ... ]` |
| `<app>_daily_history` | Historical daily log | `{ "2026-09-25": { solved: 30, accuracy: "95.0", speed: "1.20" } }` |
| `<app>_difficulty` | Selected difficulty preset | `"all"` \| `"easy"` \| `"medium"` \| `"hard"` \| `"random"` |
| `<app>_muted` | Audio toggle flag | `"true"` \| `"false"` |

---

## 6. Implementation Sync Matrix

| Feature | Math Trainer (`multiply/`) | Wortarten Trainer (`noun_verb_adjektiv/`) | I/Y Trainer (`sk_diktat/`) |
| :--- | :---: | :---: | :---: |
| **3-Column Grid** | ✅ | ✅ | ✅ |
| **Interactive Matrix** | ✅ 2D (Fact × Fact) | ✅ 1D Grid (81 Sentences) | ✅ Grid (Words) |
| **P80 Speed Sparkline** | ✅ | ✅ | ✅ |
| **20s Auto-Pause** | ✅ | ✅ | ✅ |
| **Paused Time Deduction** | ✅ | ✅ | ✅ |
| **Daily History Log** | ✅ Right pane details | ✅ Right pane details | ✅ Right pane details |
| **Reset Placement** | ✅ Inside details drawer | ✅ Inside details drawer | ✅ Inside details drawer |
| **Auto-Advance Flow** | ✅ 400ms | ✅ 500ms | ✅ 800ms |
| **Timer Guard** | ✅ | ✅ | ✅ |
| **Keyboard Shortcuts** | Enter, Numpad | 1, 2, 3, N, V, A, P, R | i, y, í, ý, H, Space |
| **Theme System** | `../css/theme.css` | `../css/theme.css` | `../css/theme.css` |
