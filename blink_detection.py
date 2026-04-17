import cv2
import time
import mediapipe as mp

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

cap = cv2.VideoCapture(0)

blink_times = []
closed_frames = 0

last_scroll_time = 0  # 🔥 cooldown timer

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:

            # Face center check
            nose = face.landmark[1]
            nose_x = int(nose.x * w)

            if nose_x < w * 0.3 or nose_x > w * 0.7:
                continue

            eye = [33, 160, 158, 133, 153, 144]

            points = []
            for idx in eye:
                x = int(face.landmark[idx].x * w)
                y = int(face.landmark[idx].y * h)
                points.append((x, y))

            eye_height = abs(points[1][1] - points[5][1])
            eye_width = abs(points[0][0] - points[3][0])

            ratio = eye_height / eye_width

            # Eye closed
            if ratio < 0.18:
                closed_frames += 1
            else:
                # Eye reopened → blink confirm
                if closed_frames >= 2:
                    current_time = time.time()
                    blink_times.append(current_time)
                    print("👁️ Blink detected")

                closed_frames = 0

    # 🔥 DOUBLE BLINK CHECK
    if len(blink_times) >= 2:
        current_time = time.time()

        # condition: 2 blinks within 1 sec + cooldown
        if (blink_times[-1] - blink_times[-2] < 1) and (current_time - last_scroll_time > 2):

            print("👉 SCROLL NEXT REEL 🔥")

            last_scroll_time = current_time   # 🔒 cooldown start
            blink_times = []                 # reset

        else:
            # remove old blink
            blink_times.pop(0)

    cv2.imshow("Blink Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()