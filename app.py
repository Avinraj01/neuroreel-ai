import cv2
import time
import webbrowser
import pyautogui
import mediapipe as mp
import threading

# 🔥 CALIBRATION
baseline_mouth = None
CALIBRATION_FRAMES = 30
calibration_data = []

from blink import detect_blink
from head import detect_head
from tracker import start_reel, end_reel, add_emotion, get_all_data
from genre_ocr import detect_genre_ocr as detect_genre_screen

# 🔥 SETTINGS
ACTION_COOLDOWN = 1.2
last_action_time = 0

current_reel_start = None
current_genre = "unknown"


# 🔥 FIXED MEDIAPIPE (LATEST VERSION COMPATIBLE)
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# 🔥 EMOTION DETECTION
def detect_emotion(face):
    global baseline_mouth, calibration_data

    left = face.landmark[61]
    right = face.landmark[291]
    top = face.landmark[13]
    bottom = face.landmark[14]

    mouth_width = abs(left.x - right.x)
    mouth_height = abs(top.y - bottom.y)

    ratio = mouth_height / (mouth_width + 1e-6)

    # 🔥 CALIBRATION
    if baseline_mouth is None:
        calibration_data.append(ratio)

        if len(calibration_data) < CALIBRATION_FRAMES:
            return "neutral"

        baseline_mouth = sum(calibration_data) / len(calibration_data)
        print("✅ Calibration Done:", baseline_mouth)
        return "neutral"

    # 🔥 DYNAMIC EMOTION
    if ratio > baseline_mouth + 0.06:
        return "happy"
    elif ratio < baseline_mouth - 0.04:
        return "sad"
    else:
        return "neutral"


# 🔥 GENRE DETECTION
def detect_genre_with_retry():
    global current_genre

    print("🎬 Detecting genre...")

    g = detect_genre_screen()

    if g == "unknown":
        print("⚠️ Retry genre...")
        time.sleep(1)
        g = detect_genre_screen()

    # 🔥 SMART FALLBACK
    if g == "unknown":
        print("⚠️ Applying smart fallback...")

        last_text_guess = current_genre.lower()

        if "song" in last_text_guess or "music" in last_text_guess:
            g = "music"
        elif "love" in last_text_guess or "heart" in last_text_guess:
            g = "love"
        elif "funny" in last_text_guess or "comedy" in last_text_guess:
            g = "comedy"
        else:
            g = current_genre

    if g != "unknown":
        current_genre = g

    print("🎯 Final Genre:", current_genre)


def detect_genre_async():
    threading.Thread(target=detect_genre_with_retry, daemon=True).start()


# 🔥 OPEN SHORTS
webbrowser.open("https://www.youtube.com/shorts")
time.sleep(7)

screen_w, screen_h = pyautogui.size()
LIKE_X = int(screen_w * 0.95)
LIKE_Y = int(screen_h * 0.5)

cap = cv2.VideoCapture(0)

# 🔥 FIRST REEL
detect_genre_async()
start_reel("unknown")
current_reel_start = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:

            # 🔥 EMOTION
            emotion = detect_emotion(face)
            add_emotion(emotion)

            # 👤 HEAD CONTROL
            nose = face.landmark[1]
            nose_y = int(nose.y * h)

            action = detect_head(nose_y)

            if action is not None and (time.time() - last_action_time > ACTION_COOLDOWN):

                print("🧠 Action:", action)

                end_reel()

                if action == "NEXT":
                    pyautogui.press("down")
                elif action == "PREVIOUS":
                    pyautogui.press("up")

                start_reel(current_genre)
                current_reel_start = time.time()

                detect_genre_async()

                last_action_time = time.time()

            # 👁️ BLINK LIKE
            eye = [33, 160, 158, 133, 153, 144]

            points = []
            for idx in eye:
                x = int(face.landmark[idx].x * w)
                y = int(face.landmark[idx].y * h)
                points.append((x, y))

            eye_height = abs(points[1][1] - points[5][1])
            eye_width = abs(points[0][0] - points[3][0])
            ratio = eye_height / eye_width

            if detect_blink(ratio):
                print("❤️ LIKE")
                pyautogui.click(screen_w//2, screen_h//2)
                time.sleep(0.2)
                pyautogui.click(LIKE_X, LIKE_Y)

    cv2.imshow("AI Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# 🔥 FINAL
cap.release()
cv2.destroyAllWindows()

end_reel()

data = get_all_data()

print("\n📊 ALL REELS DATA:")
for i, d in enumerate(data):
    print(f"\nReel {i+1}")
    print("Genre:", d["genre"])
    print("Time:", d["duration"])
    print("Happy:", d["happy"], "%")
    print("Neutral:", d["neutral"], "%")
    print("Sad:", d["sad"], "%")

from analytics import generate_dashboard
generate_dashboard(data)