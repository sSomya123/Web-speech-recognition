import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
from tensorflow.keras.models import load_model

# ======================
# CONFIG
# ======================
MODEL_PATH = "models/facial_emotion_detection_model.h5"
EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

# ======================
# LOAD MODEL
# ======================
model = load_model(MODEL_PATH)

# ======================
# TEXT TO SPEECH
# ======================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ======================
# MEDIAPIPE FACE DETECTOR
# ======================
mp_face = mp.solutions.face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.6
)

# ======================
# EMOTION PREDICTION
# ======================
def predict_emotion(face):
    try:
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (48, 48))
        normalized = resized / 255.0
        reshaped = normalized.reshape(1, 48, 48, 1)

        preds = model.predict(reshaped, verbose=0)
        return EMOTIONS[np.argmax(preds)]
    except:
        return "neutral"

# ======================
# GREETING LOGIC
# ======================
def greeting_from_emotion(emotion):
    return {
        "happy": "You look happy today!",
        "sad": "You seem a bit down. I'm here.",
        "angry": "You look upset. Take a deep breath.",
        "fear": "You seem anxious. Everything will be okay.",
        "surprise": "Oh! You look surprised!",
        "disgust": "Hmm. Something feels off.",
        "neutral": "Hello! Nice to see you."
    }.get(emotion, "Hello!")

# ======================
# MAIN LOOP
# ======================
cap = cv2.VideoCapture(0)
greeted = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face.process(rgb)

    if results.detections and not greeted:
        h, w, _ = frame.shape
        det = results.detections[0]
        box = det.location_data.relative_bounding_box

        x = int(box.xmin * w)
        y = int(box.ymin * h)
        bw = int(box.width * w)
        bh = int(box.height * h)

        face = frame[y:y+bh, x:x+bw]

        emotion = predict_emotion(face)
        greeting = greeting_from_emotion(emotion)

        print(f"Detected emotion: {emotion}")
        speak(greeting)

        greeted = True

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

