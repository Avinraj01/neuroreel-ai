import time

blink_times = []
closed_frames = 0

COOLDOWN = 2
last_blink_action = 0


def detect_blink(ratio):
    global closed_frames, blink_times, last_blink_action

    # 🔥 strict eye close
    if ratio < 0.18:
        closed_frames += 1
    else:
        # eye reopened → blink confirm
        if closed_frames >= 4:
            blink_times.append(time.time())
            print("👁️ Real Blink")

        closed_frames = 0

    # 🔥 DOUBLE BLINK CHECK
    if len(blink_times) >= 2:
        t1, t2 = blink_times[-2], blink_times[-1]

        if (t2 - t1 < 0.8) and (time.time() - last_blink_action > COOLDOWN):
            print("🔥 DOUBLE BLINK CONFIRMED")
            blink_times = []
            last_blink_action = time.time()
            return True
        else:
            blink_times.pop(0)

    return False