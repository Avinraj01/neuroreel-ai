import cv2
import time
import webbrowser
import pyautogui
import mediapipe as mp
import threading

from blink import detect_blink
from head import detect_head
from tracker import start_reel, end_reel, add_emotion, get_all_data
from genre_ocr import detect_genre_ocr as detect_genre_screen
from analytics import generate_dashboard

# 🔥 SETTINGS
ACTION_COOLDOWN = 1.2
last_action_time = 0

current_genre = "unknown"

# 🔥 EMOTION
baseline_mouth = None
calibration_data = []

# 🔥 PAUSE STATE
is_paused = False

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()


def detect_emotion(face):
    global baseline_mouth, calibration_data

    left = face.landmark[61]
    right = face.landmark[291]
    top = face.landmark[13]
    bottom = face.landmark[14]

    width = abs(left.x - right.x)
    height = abs(top.y - bottom.y)

    ratio = height / (width + 1e-6)

    if baseline_mouth is None:
        calibration_data.append(ratio)
        if len(calibration_data) < 30:
            return "neutral"
        baseline_mouth = sum(calibration_data) / len(calibration_data)
        print("✅ Emotion Calibration Done")
        return "neutral"

    if ratio > baseline_mouth + 0.05:
        return "happy"
    elif ratio < baseline_mouth - 0.04:
        return "sad"
    else:
        return "neutral"


def detect_genre_async():
    global current_genre
    g = detect_genre_screen()
    if g != "unknown":
        current_genre = g


# 🔥 OPEN SHORTS
webbrowser.open("https://www.youtube.com/shorts")
time.sleep(7)

cap = cv2.VideoCapture(0)

threading.Thread(target=detect_genre_async).start()
start_reel("unknown")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:

            # 🔥 EMOTION TRACK
            emotion = detect_emotion(face)
            add_emotion(emotion)

            # 👁️ BLINK FIRST (🔥 FIX)
            eye = [33, 160, 158, 133, 153, 144]

            pts = []
            for idx in eye:
                x = int(face.landmark[idx].x * w)
                y = int(face.landmark[idx].y * h)
                pts.append((x, y))

            eye_h = abs(pts[1][1] - pts[5][1])
            eye_w = abs(pts[0][0] - pts[3][0])
            ratio = eye_h / eye_w

            # 🔥 BLINK DETECTION
            if detect_blink(ratio):
                is_paused = not is_paused

                if is_paused:
                    print("⏸️ PAUSE")
                else:
                    print("▶️ PLAY")

                pyautogui.press("space")

                # 🔥 CRITICAL LINE
                continue   # 👈 यही main fix है

            # 👤 HEAD CONTROL (only if NO blink)
            nose = face.landmark[1]
            nose_y = int(nose.y * h)

            action = detect_head(nose_y)

            if action and (time.time() - last_action_time > ACTION_COOLDOWN):

                print("🧠 Action:", action)

                end_reel()

                if action == "NEXT":
                    pyautogui.press("down")
                elif action == "PREVIOUS":
                    pyautogui.press("up")

                start_reel(current_genre)
                threading.Thread(target=detect_genre_async).start()

                last_action_time = time.time()

    cv2.imshow("AI Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# 🔥 FINAL
cap.release()
cv2.destroyAllWindows()

end_reel()

data = get_all_data()

generate_dashboard(data)