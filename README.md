# Kubi Kids School 🎒✏️

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-2ea44f?style=for-the-badge&logo=github)](https://igorcerovsky.github.io/kids_school/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> **Live Web Application:**  
> 👉 **[https://igorcerovsky.github.io/kids_school/](https://igorcerovsky.github.io/kids_school/)**

An interactive educational portal with web applications and practice tools designed for children. Features adaptive learning algorithms, speed measurement, instant feedback, light & dark themes, and mobile-friendly layouts.

---

## 🚀 Quick Links (Direct Access)

| Application | Category | Live Link |
| :--- | :--- | :--- |
| **Main Portal Hub** | All Activities | [Open Portal](https://igorcerovsky.github.io/kids_school/) |
| **Math Trainer** (Násobilka & Aritmetika) | Mathematics | [Open Math Trainer](https://igorcerovsky.github.io/kids_school/multiply/) |
| **Division with Remainder** (Delenie so zvyškom) | Mathematics | [Open Remainder Trainer](https://igorcerovsky.github.io/kids_school/multiply/remainder.html) |
| **Zahlenpyramide** (Číselné pyramídy) | Mathematics | [Open Zahlenpyramide](https://igorcerovsky.github.io/kids_school/multiply/pyramide.html) |
| **I / Y Trenažér** (Vybrané slová B, M, P, R, S, V, Z, L) | Slovak Language | [Open I/Y Trenažér](https://igorcerovsky.github.io/kids_school/sk_diktat/iy_trainer.html) |
| **Wortarten Lernspiel** (Nomen, Verben, Adjektive) | German Language | [Open Wortarten](https://igorcerovsky.github.io/kids_school/noun_verb_adjektiv/) |
| **Tasteninstrumente Quiz** (Klávesové nástroje) | Music Education | [Open Quiz 1](https://igorcerovsky.github.io/kids_school/musik/instrumente_1.html) |
| **Saiteninstrumente Quiz 1** (Strunové nástroje) | Music Education | [Open Quiz 2](https://igorcerovsky.github.io/kids_school/musik/instrumente_2.html) |
| **Saiteninstrumente Quiz 2** (Strunové nástroje) | Music Education | [Open Quiz 3](https://igorcerovsky.github.io/kids_school/musik/instrumente_3.html) |

---

## 🌟 Key Applications

### ✖️ Math Trainer (`/multiply/`)
An intelligent arithmetic practice app featuring:
- **Operations**: Multiplication (`✖`), Addition (`➕`), Subtraction (`➖`), and Division (`➗`) with exclusive operation modes and custom number ranges for each operation (`[0–10]`, `[1–10]`, `[3–9]`).
- **Adaptive Spaced Practice**: Focus on the slowest problems or repeated practice of mistakes.
- **Smart Input Flow**: Automatically advances to the next problem as soon as the correct answer is typed. Configurable wrong-answer timer (marks incorrect and proceeds if wrong after $N$ seconds).
- **Interactive Matrix & Heatmap**: Visual grid showing unpracticed, mastered, and slow problem facts with live response-time statistics.
- **Multilingual UI**: Switch seamlessly between Slovak (**SK**), English (**EN**), and German (**DE**).

### ➗ Division with Remainder (`/multiply/remainder.html`)
Dedicated trainer for integer division with remainders:
- **Dual-Input Stage**: Separate inputs for quotient and remainder ($a \div b = q \text{ rem } r$).
- **Smart 3-Second Flow**: Auto-advances immediately on correct quotient or after 3 seconds on an incorrect quotient attempt.
- **Remainder Matrix (Matica delenia so zvyškom)**: Visual 2D matrix displaying mastery and speed across dividend and divisor dimensions, perfectly scaled to fit the side pane.
- **Quick Presets**: Fast switching between `[2–10]` and `[3–9]` divisor ranges.

### 🇸🇰 Slovak Orthography (`/sk_diktat/`)
- Adaptive reinforcement for Slovak *vybrané slová* (i/y after B, M, P, R, S, V, Z, L).
- Speech synthesis for full sentence dictation with word-by-word correctness verification.

### 🇩🇪 German Grammar (`/noun_verb_adjektiv/`)
- Interactive classification game teaching German parts of speech (*Nomen, Verben, Adjektive*).

### 🎵 Music Education (`/musik/`)
- Visual quizzes identifying musical instruments (keyboard and string families).

---

## 💻 Local Development

No build tools or bundlers are required. The project consists of standard HTML5, CSS3, and modern Vanilla JavaScript.

To run the app locally:

```bash
# Clone the repository
git clone https://github.com/igorcerovsky/kids_school.git
cd kids_school

# Start any local HTTP server (e.g. Python 3)
python3 -m http.server 8080

# Open in your browser
open http://localhost:8080
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
