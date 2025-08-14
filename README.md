---
💎 GemRush

GemRush is a fast-paced arcade-style OpenGL game where your goal is to catch falling gems using a basket.
The game tests your reflexes and precision as the gems drop faster with every successful catch.

---

## 📜 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running the Game](#running-the-game)
6. [Gameplay Instructions](#gameplay-instructions)

   * [Controls](#controls)
   * [Objective](#objective)
   * [Game Over Conditions](#game-over-conditions)
   * [Scoring](#scoring)
7. [Game Screen Layout](#game-screen-layout)
8. [Tips & Tricks](#tips--tricks)
9. [License](#license)

---

## 📖 Overview

In **GemRush**, sparkling gems fall from the top of the screen, and you control a basket at the bottom to catch them.
The more gems you catch, the faster they fall.
If you miss a gem, the game ends, and you can restart or quit via the on-screen buttons.

---

## ✨ Features

* 🎯 **Smooth real-time gameplay** at 60 FPS
* 💎 **Rotating and sparkling gem visuals**
* 🛑 **Pause, restart, and quit buttons** built into the UI
* 📈 **Progressive difficulty** — gems fall faster as your score increases
* 🎨 Custom **OpenGL rendering** with perspective and shape details

---

## 🖥 Requirements

* Python 3.x
* **PyOpenGL**
* **PyOpenGL\_accelerate** *(optional for better performance)*

---

## ⚙ Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/gemrush.git
cd gemrush

# Install dependencies
pip install PyOpenGL PyOpenGL_accelerate
```

---

## ▶ Running the Game

```bash
python gemrush.py
```

---

## 🎮 Gameplay Instructions

### 🎛 Controls

| Action                   | Key/Mouse                                     |
| ------------------------ | --------------------------------------------- |
| Move basket left         | ← (Left Arrow)                                |
| Move basket right        | → (Right Arrow)                               |
| Pause/Resume             | Spacebar                                      |
| Restart game (UI button) | Left-click on **blue circle** at top left     |
| Quit game (UI button)    | Left-click on **red X** at top right          |
| Pause/Resume (UI button) | Left-click on **orange button** at top center |

---

### 🎯 Objective

* **Catch falling gems** with your basket before they hit the ground.
* Each successful catch increases your score and makes the gems fall faster.

---

### 💀 Game Over Conditions

* You **miss a gem** (it falls past the basket).
* The basket turns **red** when the game ends.
* You can restart via the blue restart button or quit via the red exit button.

---

### 🏆 Scoring

* **+1 point** for every gem caught.
* Gems fall **faster** with each point scored.

---

## 🖼 Game Screen Layout

```
 -------------------------------------------------
|  🔄 (Restart)   ⏸ (Pause/Resume)   ❌ (Exit)    |
|                                                  |
|         Falling gems appear here                 |
|                                                  |
|                                                  |
|                      Basket                      |
 -------------------------------------------------
```

---

## 💡 Tips & Tricks

* **Anticipate gem movement** — they drop faster over time.
* Use **pause** to regain focus during intense gameplay.
* Keep your basket **centered** when waiting for the next gem.

---

## 📜 License

This project is licensed under the MIT License.

---

