
import cv2
import mediapipe as mp
import time
import math
from collections import deque, Counter
from threading import Thread, Lock

# Shared state
latest_greeting = None
lock = Lock()

# ===============================
# EMOTION UTILS
# ===============================
def dist(p1, p2):
    return math.dist(p1, p2)

def detect_emotion(landmarks):
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]

    eye_top = landmarks[159]
    eye_bottom = landmarks[145]

    eyebrow = landmarks[105]
    eye_center = landmarks[33]

    mouth_width = dist(left_mouth, right_mouth)
    mouth_open = dist(top_lip, bottom_lip)
    eye_open = dist(eye_top, eye_bottom)
    brow_dist = dist(eyebrow, eye_center)

    mouth_ratio = mouth_open / mouth_width
    eye_ratio = eye_open / mouth_width
    brow_ratio = brow_dist / mouth_width

    if mouth_ratio > 0.30:
        return "surprised"
    elif mouth_ratio > 0.18:
        return "happy"
    elif brow_ratio < 0.07:
        return "angry"
    elif eye_ratio < 0.03:
        return "sad"
    else:
        return "neutral"

def greeting_from_emotion(emotion):
    return {
        "happy": "You look happy today. Welcome to our hospital.",
        "surprised": "Hello! You seem surprised. How may I help you?",
        "sad": "Hello. If you’re feeling low, I’m here to help.",
        "angry": "Hello. Take a breath. I’m here to assist you.",
        "neutral": "Hello! Welcome to our hospital assistant."
    }.get(emotion, "Hello!")

# ===============================
# BACKGROUND THREAD
# ===============================
def start_emotion_engine():
    global latest_greeting

    cap = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    smoother = deque(maxlen=15)
    greeted = False

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks and not greeted:
                h, w, _ = frame.shape
                landmarks = [
                    (int(lm.x * w), int(lm.y * h))
                    for lm in results.multi_face_landmarks[0].landmark
                ]

                emotion = detect_emotion(landmarks)
                smoother.append(emotion)
                stable_emotion = Counter(smoother).most_common(1)[0][0]

                with lock:
                    latest_greeting = greeting_from_emotion(stable_emotion)

                greeted = True   # greet once per server run

            time.sleep(0.05)
