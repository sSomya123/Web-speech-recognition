# nlp_model.py
# NLP Model for hospital assistant chatbot

import json
import re
from difflib import SequenceMatcher
import random

class HospitalNLPModel:
    def __init__(self, training_data_path='training_data.json'):
        """Initialize the NLP model with training data from JSON file"""
        self.training_data_path = training_data_path
        self.intents = []
        self.default_response = ""
        self.load_training_data()
        
    def load_training_data(self):
        """Load training data from JSON file"""
        try:
            with open(self.training_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.intents = data.get('intents', [])
                self.default_response = data.get('default_response', 
                    "I'm here to help with appointments and hospital information. Could you please rephrase?")
                print(f"✓ Loaded {len(self.intents)} intent categories from training data")
        except FileNotFoundError:
            print(f"Error: {self.training_data_path} not found!")
            self.default_response = "Training data not loaded. Please contact support."
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {self.training_data_path}: {e}")
            self.default_response = "Training data format error. Please contact support."
    
    def preprocess_text(self, text):
        """Clean and normalize input text"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity ratio between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_intent(self, user_input):
        """Find the best matching intent from training data"""
        user_input = self.preprocess_text(user_input)
        best_intent = None
        highest_score = 0.0
        threshold = 0.4  # Minimum similarity threshold
        
        for intent in self.intents:
            for pattern in intent['patterns']:
                pattern_clean = self.preprocess_text(pattern)
                
                # Check for exact phrase match
                if pattern_clean in user_input or user_input in pattern_clean:
                    score = 0.9
                else:
                    # Calculate similarity score
                    score = self.calculate_similarity(user_input, pattern_clean)
                
                # Check for keyword presence
                pattern_words = set(pattern_clean.split())
                user_words = set(user_input.split())
                common_words = pattern_words.intersection(user_words)
                
                if common_words:
                    word_match_score = len(common_words) / max(len(pattern_words), len(user_words))
                    score = max(score, word_match_score)
                
                if score > highest_score:
                    highest_score = score
                    best_intent = intent
        
        # Return best intent if above threshold
        if highest_score >= threshold and best_intent:
            return best_intent
        else:
            return None
    
    def get_response(self, user_input):
        """Main method to get response for user input"""
        if not user_input or not user_input.strip():
            return "I didn't catch that. Could you please repeat?"
        
        intent = self.find_intent(user_input)
        
        if intent:
            # Return a random response from the intent's responses
            return random.choice(intent['responses'])
        else:
            return self.default_response
    
    def is_greeting(self, user_input):
        """Check if input is a greeting"""
        intent = self.find_intent(user_input)
        return intent and intent['tag'] == 'greeting'
    
    def is_diagnosis_query(self, user_input):
        """Check if user is asking for diagnosis"""
        intent = self.find_intent(user_input)
        return intent and intent['tag'] in ['diagnosis', 'symptoms', 'medication']
    
    def reload_training_data(self):
        """Reload training data from JSON file (useful for updates)"""
        self.load_training_data()
        return f"Training data reloaded successfully. {len(self.intents)} intents loaded."
