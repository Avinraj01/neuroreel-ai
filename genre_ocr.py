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
    print("📸 Capturing OPTIMIZED SHORTS AREA...")

    screen_w, screen_h = pyautogui.size()

    # 🔥🔥 SHIFTED UP (20% FIX)
    region = (
        int(screen_w * 0.35),   # left (center)
        int(screen_h * 0.20),   # 🔥 moved UP (was 0.10)
        int(screen_w * 0.30),   # width (center strip)
        int(screen_h * 0.65)    # 🔥 reduced height (was 0.75)
    )

    img = pyautogui.screenshot(region=region)
    img.save("debug.png")

    # 🔥 preprocess
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # better threshold
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)

    # 🔥 OCR config
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    text = clean_text(text)

    print("📝 OCR Clean Text:", text)

    if len(text) < 5:
        return "unknown"

    result = classifier(text, labels)
    genre = result["labels"][0]

    print("🎯 Genre:", genre)

    return genre