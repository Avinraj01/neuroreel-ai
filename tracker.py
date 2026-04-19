import time

current_reel = {
    "genre": None,
    "start_time": None,
    "emotions": []
}

all_reels = []


def start_reel(genre):
    current_reel["genre"] = genre
    current_reel["start_time"] = time.time()
    current_reel["emotions"] = []


def add_emotion(emotion):
    current_reel["emotions"].append(emotion)


def end_reel():
    duration = time.time() - current_reel["start_time"]
    emotions = current_reel["emotions"]

    if len(emotions) > 0:
        total = len(emotions)

        happy = emotions.count("happy") / total * 100
        neutral = emotions.count("neutral") / total * 100
        sad = emotions.count("sad") / total * 100
    else:
        happy = neutral = sad = 0

    all_reels.append({
        "genre": current_reel["genre"],
        "duration": round(duration, 2),
        "happy": round(happy, 2),
        "neutral": round(neutral, 2),
        "sad": round(sad, 2)
    })


def get_all_data():
    return all_reels