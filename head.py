import time
from collections import deque

history = deque(maxlen=7)

state = "NEUTRAL"
neutral_y = None

last_action_time = 0
COOLDOWN = 1.5

UP_THRESHOLD = -40
DOWN_THRESHOLD = 40
RETURN_RANGE = 10


def detect_head(nose_y):
    global state, neutral_y, last_action_time

    history.append(nose_y)
    smooth_y = sum(history) / len(history)

    # set baseline
    if neutral_y is None:
        neutral_y = smooth_y
        return None

    # cooldown
    if time.time() - last_action_time < COOLDOWN:
        return None

    diff = smooth_y - neutral_y

    action = None

    # 🔼 detect UP movement
    if diff < UP_THRESHOLD:
        if state == "NEUTRAL":
            state = "UP"

    # 🔽 detect DOWN movement
    elif diff > DOWN_THRESHOLD:
        if state == "NEUTRAL":
            state = "DOWN"

    # 🎯 CONFIRM ONLY WHEN RETURN TO CENTER
    elif abs(diff) < RETURN_RANGE:

        if state == "UP":
            action = "NEXT"
            print("✅ UP → NEXT")
            last_action_time = time.time()

        elif state == "DOWN":
            action = "PREVIOUS"
            print("✅ DOWN → PREVIOUS")
            last_action_time = time.time()

        state = "NEUTRAL"

    return action