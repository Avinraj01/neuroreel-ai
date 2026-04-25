# 🧠 NeuroReel AI

> 🚀 AI-powered **Hands-Free YouTube Shorts Controller** with real-time analytics
> Built using **Computer Vision + AI + OCR + Emotion Tracking**

---

![Demo](assets/neuroreel.gif)

---

## 📛 Badges

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-enabled-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-face--tracking-orange)
![AI](https://img.shields.io/badge/AI-ComputerVision-purple)
![Status](https://img.shields.io/badge/status-active-success)

---

## 🧠 Project Mindmap

```mermaid
mindmap
  root((NeuroReel AI))
    Input
      Webcam
      Screen Capture
    Detection
      Eye Blink -> Pause/Play
      Head Movement -> Scroll
      Emotion -> Happy Neutral Sad
    OCR
      Caption Extraction
      Text Cleaning
    AI Model
      Transformer Classification
      Genre Prediction
    Tracking
      Time Spent
      Emotion Logs
    Output
      Dashboard
      Graphs
      Insights
```

---

## 🔄 Workflow

```mermaid
flowchart TD
    A[Webcam Input] --> B[Face Detection]
    B --> C[Eye Blink Detection]
    B --> D[Head Movement Detection]
    C --> E[Pause or Play]
    D --> F[Scroll Next or Previous]
    F --> G[OCR Caption Capture]
    G --> H[Genre Detection]
    B --> I[Emotion Detection]
    H --> J[Tracking System]
    I --> J
    J --> K[Analytics Dashboard]
```

---

## 📂 Project Structure

```
neuroreel-ai/
│
├── app.py              ← Main controller
├── blink.py            ← Eye blink logic
├── head.py             ← Head movement logic
├── genre_ocr.py        ← OCR + genre detection
├── tracker.py          ← Data tracking
├── analytics.py        ← Dashboard generation
│
├── assets/
│   └── neuroreel.gif   ← Demo animation
│
├── requirements.txt
├── README.md
```

---

## ⚡ Features

* 👁️ Double Blink → Pause / Play
* 👤 Head Up / Down → Next / Previous Shorts
* 🧠 Emotion Detection (Happy / Neutral / Sad)
* 🔍 OCR-based Caption Analysis
* 🎯 Genre Classification using Transformers
* 📊 Auto-generated Analytics Dashboard
* ⚡ Real-time processing

---

## 🛠 Tech Stack

* Python
* OpenCV
* MediaPipe
* Transformers (HuggingFace)
* Tesseract OCR
* PyAutoGUI
* Matplotlib

---

## 🚀 Quickstart

### 1️⃣ Clone the repo

```bash
git clone https://github.com/Avinraj01/neuroreel-ai.git
cd neuroreel-ai
```

---

### 2️⃣ Create virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run project

```bash
python app.py
```

---

## 📊 Output

* 🎬 Hands-free Shorts control
* 🧠 Emotion tracking
* 📈 Graph (Emotion Trend)
* 📄 dashboard.html auto-generated

---

## 🧠 Future Improvements

* 🎙 Voice command support
* 📱 Mobile integration
* ☁️ Cloud dashboard
* 🤖 Better emotion accuracy

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch (`git checkout -b feature-name`)
3. Commit (`git commit -m "New feature"`)
4. Push (`git push origin feature-name`)
5. Open Pull Request 🚀

---

## 📜 License

MIT License

---
![Demo](assets/Readme_Bottom.gif)

---
✨ *AI + Vision + Automation = Future Interaction* ✨
