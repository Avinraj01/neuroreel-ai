import pyautogui
import pytesseract
import cv2
import numpy as np
from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    framework="pt"
)

labels = ["comedy", "love", "motivation", "music", "education", "gaming"]

def clean_text(t):
    t = t.lower()
    bad = ["share", "subscribe", "like", "follow", "comments"]
    for b in bad:
        t = t.replace(b, "")
    return t.strip()

def detect_genre_ocr():
    print("📸 Capturing CAPTION AREA...")

    screen_w, screen_h = pyautogui.size()

    # 🔥 slightly tighter caption region
    region = (
        int(screen_w * 0.30),
        int(screen_h * 0.70),
        int(screen_w * 0.40),
        int(screen_h * 0.20)
    )

    img = pyautogui.screenshot(region=region)
    img.save("debug.png")

    # 🔥 preprocess for better OCR
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)

    text = clean_text(text)

    print("📝 OCR Clean Text:", text)

    if len(text) < 5:
        return "unknown"

    result = classifier(text, labels)
    genre = result["labels"][0]

    print("🎯 Genre:", genre)
    return genre