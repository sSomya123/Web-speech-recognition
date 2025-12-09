# main.py
# Flask application for Hospital Voice Assistant

from flask import Flask, render_template_string, request, jsonify
from nlp_model import HospitalNLPModel
import os

app = Flask(__name__)

# Initialize NLP model with JSON training data
nlp_model = HospitalNLPModel('./data/training_data.json')

# HTML Template with Speech Recognition and Text-to-Speech
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Voice Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .assistant-icon {
            width: 120px;
            height: 120px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 80%;
            word-wrap: break-word;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .bot-message {
            background: #e8eaf6;
            color: #333;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        #userInput {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #userInput:focus {
            border-color: #667eea;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-voice {
            background: #4CAF50;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .btn-voice:hover {
            background: #45a049;
        }
        
        .btn-voice.listening {
            background: #f44336;
            animation: recordPulse 1s infinite;
        }
        
        @keyframes recordPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        
        .status {
            text-align: center;
            margin-top: 15px;
            color: #666;
            font-size: 14px;
        }
        
        .listening-indicator {
            color: #f44336;
            font-weight: bold;
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="assistant-icon">🏥</div>
            <h1>Hospital Assistant</h1>
            <p>Your AI-powered healthcare companion</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot-message">
                Hello! Welcome to our hospital. I'm here to help you with appointments and information. How may I assist you today?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type your message or use voice..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="btn btn-primary" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="controls">
            <button class="btn-voice" id="voiceBtn" onclick="toggleVoice()">🎤</button>
        </div>
        
        <div class="status" id="status">Click the microphone to speak</div>
    </div>

    <script>
        let recognition;
        let isListening = false;
        let synthesis = window.speechSynthesis;
        
        // Initialize Speech Recognition
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isListening = true;
                document.getElementById('voiceBtn').classList.add('listening');
                document.getElementById('status').innerHTML = 
                    '<span class="listening-indicator">🔴 Listening...</span>';
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                document.getElementById('userInput').value = transcript;
                sendMessage();
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('status').innerHTML = 
                    'Error: ' + event.error + '. Please try again.';
                stopListening();
            };
            
            recognition.onend = function() {
                stopListening();
            };
        } else {
            document.getElementById('status').innerHTML = 
                '<div class="error">Speech recognition not supported in this browser. Please use Chrome.</div>';
        }
        
        function toggleVoice() {
            if (isListening) {
                recognition.stop();
            } else {
                recognition.start();
            }
        }
        
        function stopListening() {
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
            document.getElementById('status').textContent = 'Click the microphone to speak';
        }
        
        function speak(text) {
            // Cancel any ongoing speech
            synthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            // Use a more natural voice if available
            const voices = synthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.lang === 'en-US' && voice.name.includes('Google')
            ) || voices.find(voice => voice.lang === 'en-US') || voices[0];
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            utterance.onstart = function() {
                document.getElementById('status').textContent = '🔊 Speaking...';
            };
            
            utterance.onend = function() {
                document.getElementById('status').textContent = 'Click the microphone to speak';
            };
            
            synthesis.speak(utterance);
        }
        
        function addMessage(message, isUser) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = message;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, true);
            input.value = '';
            
            try {
                // Send to backend
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Add bot response to chat
                addMessage(data.response, false);
                
                // Speak the response
                speak(data.response);
                
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        }
        
        // Load voices when they become available
        if (synthesis.onvoiceschanged !== undefined) {
            synthesis.onvoiceschanged = function() {
                synthesis.getVoices();
            };
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Get response from NLP model
        bot_response = nlp_model.get_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'response': 'I apologize, but I encountered an error. Please try again.',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/reload', methods=['POST'])
def reload_training_data():
    """Endpoint to reload training data without restarting server"""
    try:
        message = nlp_model.reload_training_data()
        return jsonify({
            'status': 'success',
            'message': message
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 Starting Hospital Voice Assistant...")
    print("=" * 60)
    
    # Check if training data file exists
    if not os.path.exists('training_data.json'):
        print("⚠️  WARNING: training_data.json not found!")
        print("Please ensure training_data.json is in the same directory.")
    else:
        print("✓ Training data loaded successfully")
    
    print("\n📋 Application Information:")
    print(f"   - NLP Model: Custom Pattern Matching")
    print(f"   - Training Data: training_data.json")
    print(f"   - Intents Loaded: {len(nlp_model.intents)}")
    
    print("\n🌐 Server Starting...")
    print("   Open your browser and navigate to: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
