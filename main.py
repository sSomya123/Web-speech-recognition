# main.py
# Flask application for Hospital Voice Assistant
# Integrated with MediaPipe-based face emotion greeting

from flask import Flask, render_template_string, request, jsonify
from nlp_model import HospitalNLPModel
from threading import Thread
import os

# Face emotion engine (background)
from face_emotion import start_emotion_engine, latest_greeting, lock

app = Flask(__name__)

# ===============================
# NLP MODEL INIT
# ===============================
nlp_model = HospitalNLPModel('./data/training_data.json')

# ===============================
# START FACE EMOTION THREAD
# ===============================
emotion_thread = Thread(target=start_emotion_engine, daemon=True)
emotion_thread.start()

# ===============================
# HTML TEMPLATE
# ===============================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hospital Voice Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            border-radius: 16px;
            padding: 30px;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }

        .chat-container {
            height: 380px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            background: #f9f9f9;
            margin-bottom: 15px;
        }

        .message {
            padding: 10px 14px;
            margin-bottom: 10px;
            border-radius: 14px;
            max-width: 75%;
        }

        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }

        .bot-message {
            background: #e8eaf6;
            color: #333;
        }

        .input-container {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 12px;
            border-radius: 20px;
            border: 1px solid #ccc;
        }

        button {
            padding: 12px 20px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            background: #667eea;
            color: white;
            font-weight: bold;
        }

        #voiceBtn {
            margin-top: 15px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            font-size: 22px;
        }

        .status {
            margin-top: 10px;
            text-align: center;
            font-size: 14px;
            color: #555;
        }
    </style>
</head>

<body>
<div class="container">
    <h2 style="text-align:center;">🏥 Hospital Assistant</h2>

    <div class="chat-container" id="chatContainer">
        <div class="message bot-message">
            Hello! Welcome to our hospital. How may I assist you today?
        </div>
    </div>

    <div class="input-container">
        <input id="userInput" placeholder="Type or speak..." 
               onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()">Send</button>
    </div>

    <div style="text-align:center;">
        <button id="voiceBtn" onclick="toggleVoice()">🎤</button>
    </div>

    <div class="status" id="status">Click the microphone to speak</div>
</div>

<script>
let recognition;
let isListening = false;
let synthesis = window.speechSynthesis;

// ===============================
// SPEECH RECOGNITION
// ===============================
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isListening = true;
        document.getElementById('status').innerText = "Listening...";
    };

    recognition.onresult = (event) => {
        document.getElementById('userInput').value = event.results[0][0].transcript;
        sendMessage();
    };

    recognition.onend = () => {
        isListening = false;
        document.getElementById('status').innerText = "Click the microphone to speak";
    };
}

function toggleVoice() {
    if (isListening) recognition.stop();
    else recognition.start();
}

// ===============================
// SPEECH SYNTHESIS
// ===============================
function speak(text) {
    synthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.9;
    synthesis.speak(utter);
}

// ===============================
// CHAT UI
// ===============================
function addMessage(msg, isUser) {
    const div = document.createElement("div");
    div.className = "message " + (isUser ? "user-message" : "bot-message");
    div.textContent = msg;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById("userInput");
    const msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, true);
    input.value = "";

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    addMessage(data.response, false);
    speak(data.response);
}

// ===============================
// ✅ EMOTION-BASED GREETING
// ===============================
window.addEventListener("load", async () => {
    try {
        const res = await fetch("/greeting");
        const data = await res.json();
        if (data.greeting) {
            addMessage(data.greeting, false);
            speak(data.greeting);
        }
    } catch (e) {
        console.error(e);
    }
});
</script>
</body>
</html>
'''

# ===============================
# ROUTES
# ===============================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/greeting')
def greeting():
    with lock:
        return jsonify({"greeting": latest_greeting})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_response = nlp_model.get_response(user_message)
    return jsonify({'response': bot_response})

# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Hospital Voice Assistant starting...")
    print("🌐 http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

