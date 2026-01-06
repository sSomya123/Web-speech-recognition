import cv2
import mediapipe as mp
import time
import math
from collections import deque, Counter

# ===============================
# CONFIG
# ===============================
CAMERA_INDEX = 0
EMOTION_WINDOW = 15          # smoothing window
GREETING_COOLDOWN = 15       # seconds
DEBUG_DRAW = True            # set False for headless mode

# ===============================
# MEDIAPIPE INIT
# ===============================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ===============================
# UTILS
# ===============================
def dist(p1, p2):
    return math.dist(p1, p2)

# ===============================
# EMOTION DETECTION (GEOMETRY BASED)
# ===============================
def detect_emotion(landmarks):
    """
    landmarks: list of (x, y) pixel points (length 468)
    """

    # Mouth
    left_mouth = landmarks[61]
    right_mouth = landmarks[291]
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]

    # Eye
    eye_top = landmarks[159]
    eye_bottom = landmarks[145]

    # Eyebrow
    eyebrow = landmarks[105]
    eye_center = landmarks[33]

    mouth_width = dist(left_mouth, right_mouth)
    mouth_open = dist(top_lip, bottom_lip)
    eye_open = dist(eye_top, eye_bottom)
    brow_dist = dist(eyebrow, eye_center)

    # Normalize
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

# ===============================
# EMOTION SMOOTHER
# ===============================
class EmotionSmoother:
    def __init__(self, size=15):
        self.buffer = deque(maxlen=size)

    def update(self, emotion):
        self.buffer.append(emotion)
        return Counter(self.buffer).most_common(1)[0][0]

# ===============================
# GREETING LOGIC
# ===============================
def greeting_from_emotion(emotion):
    greetings = {
        "happy": "You look happy today. Hello!",
        "surprised": "Oh! You look surprised. Hello there!",
        "sad": "Hey… everything okay? I'm here.",
        "angry": "Hello. Take a breath, no rush.",
        "neutral": "Hello! How can I help you?"
    }
    return greetings.get(emotion, "Hello!")

# ===============================
# TTS HOOK (REPLACE WITH YOUR OWN)
# ===============================
def speak(text):
    """
    Replace this with:
    - pyttsx3
    - gTTS
    - WebSocket to browser speech
    """
    print(f"[SPEAK]: {text}")

# ===============================
# MAIN LOOP
# ===============================
def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    smoother = EmotionSmoother(EMOTION_WINDOW)

    greeted = False
    last_greet = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        emotion = "neutral"

        if result.multi_face_landmarks:
            face_landmarks = result.multi_face_landmarks[0]
            h, w, _ = frame.shape

            points = [
                (int(lm.x * w), int(lm.y * h))
                for lm in face_landmarks.landmark
            ]

            emotion = detect_emotion(points)
            stable_emotion = smoother.update(emotion)

            if DEBUG_DRAW:
                cv2.putText(
                    frame,
                    f"Emotion: {stable_emotion}",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            # Greeting trigger
            if not greeted and time.time() - last_greet > GREETING_COOLDOWN:
                greeting = greeting_from_emotion(stable_emotion)
                speak(greeting)
                greeted = True
                last_greet = time.time()

        if DEBUG_DRAW:
            cv2.imshow("Emotion Greeting Assistant", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    main()
