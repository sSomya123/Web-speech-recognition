# training_data.py
# Training dataset for hospital appointment assistant

TRAINING_DATA = [
    # Greetings
    {"pattern": "hello", "response": "Hello! Welcome to our hospital. How may I assist you today?", "tag": "greeting"},
    {"pattern": "hi", "response": "Hi there! I'm your hospital assistant. How can I help you?", "tag": "greeting"},
    {"pattern": "hey", "response": "Hey! Welcome to our medical facility. What can I do for you?", "tag": "greeting"},
    {"pattern": "good morning", "response": "Good morning! How may I assist you with your healthcare needs today?", "tag": "greeting"},
    {"pattern": "good afternoon", "response": "Good afternoon! Welcome to our hospital. How can I help you?", "tag": "greeting"},
    {"pattern": "good evening", "response": "Good evening! I'm here to assist you. What do you need help with?", "tag": "greeting"},
    
    # Appointments
    {"pattern": "book appointment", "response": "I can help you book an appointment. Which department would you like to visit? We have Cardiology, Orthopedics, Pediatrics, General Medicine, and more.", "tag": "appointment"},
    {"pattern": "schedule appointment", "response": "I'd be happy to schedule an appointment for you. What type of specialist would you like to see?", "tag": "appointment"},
    {"pattern": "make appointment", "response": "Sure! Let me help you make an appointment. Which doctor or department are you looking for?", "tag": "appointment"},
    {"pattern": "appointment availability", "response": "I can check appointment availability for you. Please specify the department or doctor you'd like to see.", "tag": "appointment"},
    {"pattern": "cancel appointment", "response": "I understand you need to cancel an appointment. Please provide your appointment ID or patient number.", "tag": "appointment"},
    {"pattern": "reschedule appointment", "response": "I can help you reschedule. Please provide your current appointment details.", "tag": "appointment"},
    {"pattern": "appointment time", "response": "Our appointment slots are available from 9 AM to 5 PM on weekdays, and 9 AM to 1 PM on Saturdays.", "tag": "appointment"},
    
    # Hospital Information
    {"pattern": "visiting hours", "response": "Our visiting hours are from 4 PM to 7 PM daily. ICU visiting hours are restricted to 30 minutes twice a day.", "tag": "info"},
    {"pattern": "hospital location", "response": "We are located at the city center, easily accessible by public transport. Would you like directions?", "tag": "info"},
    {"pattern": "departments", "response": "We have Cardiology, Neurology, Orthopedics, Pediatrics, General Surgery, Obstetrics, Emergency Care, and many more departments.", "tag": "info"},
    {"pattern": "emergency", "response": "For emergencies, please call our emergency hotline immediately or visit our 24/7 emergency department. This is not for emergency situations.", "tag": "info"},
    {"pattern": "contact number", "response": "You can reach our main reception at our contact number. For appointments, you can also use this assistant.", "tag": "info"},
    
    # Diagnosis Queries (Redirect to Doctor)
    {"pattern": "diagnosis", "response": "I'm not designed to provide medical diagnosis. Please consult with a doctor for accurate diagnosis. Would you like to book an appointment?", "tag": "diagnosis"},
    {"pattern": "what disease", "response": "I cannot diagnose medical conditions. Please contact a qualified doctor for proper diagnosis. Shall I help you schedule an appointment?", "tag": "diagnosis"},
    {"pattern": "symptoms", "response": "I'm not qualified to interpret symptoms or provide diagnosis. Please consult with our doctors. Would you like to book an appointment?", "tag": "diagnosis"},
    {"pattern": "pain", "response": "I'm unable to diagnose or advise on pain-related issues. Please consult with a doctor immediately. Can I help you schedule an urgent appointment?", "tag": "diagnosis"},
    {"pattern": "medicine", "response": "I cannot recommend medications. Please consult with a doctor for proper medical advice. Would you like to see a doctor?", "tag": "diagnosis"},
    {"pattern": "treatment", "response": "Treatment plans should be discussed with a qualified physician. I'm not designed to provide medical advice. Can I book an appointment for you?", "tag": "diagnosis"},
    {"pattern": "fever", "response": "I cannot provide medical diagnosis. Please consult with our doctors regarding your fever. Would you like to book an appointment?", "tag": "diagnosis"},
    {"pattern": "headache", "response": "For medical concerns like headaches, please consult a doctor. I can help you schedule an appointment if you'd like.", "tag": "diagnosis"},
    
    # Patient Records
    {"pattern": "medical records", "response": "For accessing medical records, please visit the reception with your patient ID. Would you like me to help with anything else?", "tag": "records"},
    {"pattern": "test results", "response": "Test results can be collected from the lab or accessed through our patient portal. Do you need help with anything else?", "tag": "records"},
    {"pattern": "prescription", "response": "For prescription refills or copies, please contact your doctor or visit the pharmacy. Can I assist with booking an appointment?", "tag": "records"},
    
    # Gratitude
    {"pattern": "thank you", "response": "You're welcome! Is there anything else I can help you with?", "tag": "thanks"},
    {"pattern": "thanks", "response": "Happy to help! Feel free to ask if you need anything else.", "tag": "thanks"},
    
    # Goodbye
    {"pattern": "bye", "response": "Goodbye! Take care and stay healthy. Feel free to return if you need assistance.", "tag": "goodbye"},
    {"pattern": "goodbye", "response": "Goodbye! Wishing you good health. Don't hesitate to reach out if you need help.", "tag": "goodbye"},
    {"pattern": "see you", "response": "See you! Stay well and come back anytime you need assistance.", "tag": "goodbye"},
]

# Default response for unrecognized queries
DEFAULT_RESPONSE = "I'm here to help with appointments and hospital information. Could you please rephrase your question, or let me know if you'd like to book an appointment?"
