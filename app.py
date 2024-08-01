from flask import Flask, render_template, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import requests
import json

app = Flask(__name__)

# Azure Speech API and OpenAI API credentials
AZURE_SPEECH_KEY = "5b33a97d32f745e09cc5b955e4f1120e"
AZURE_SPEECH_REGION = "southeastasia"
API_KEY = 'ee663c94e2384769a782442342bf3a56'
ENDPOINT = 'https://bobthebuilder001.openai.azure.com/'
DEPLOYMENT_NAME = 'gpt-35-turbo'

# Setup for Azure Speech-to-Text
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Function to recognize speech
def recognize_speech():
    try:
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        return speech_recognition_result.text
    except Exception as e:
        print("Mic is not available. Please check your microphone settings.")
        return None

# Function to get chatbot response from Azure OpenAI
def get_chatbot_response(user_input):
    headers = {
        'Content-Type': 'application/json',
        'api-key': API_KEY,
    }

    data = {
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 1.0,
        "n": 1,
        "stop": None
    }
    
    url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2023-05-15"
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to synthesize speech
def synthesize_speech(text):
    try:
        audio_config = speechsdk.audio.AudioOutConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        return speech_synthesis_result
    except Exception as e:
        print("Error with speech synthesis. Please try again later.")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response_text = get_chatbot_response(user_input)
    if response_text:
        synthesize_speech(response_text)
        return jsonify({'message': response_text})
    return jsonify({'message': 'Error generating response'})

if __name__ == '__main__':
    app.run(debug=True)
