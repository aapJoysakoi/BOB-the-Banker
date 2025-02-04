import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import requests
import json

# Custom CSS
custom_css = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
        }
        .custom-title {
            color: #075E54;
            font-size: 2em;
            text-align: center;
            margin-bottom: 20px;
        }
        .chat-window {
            background-color: #ffffff;
            border: 1px solid #CCC;
            border-radius: 10px;
            width: 100%;
            max-width: 500px;
            height: 60vh;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
        }
        .chat-history {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: #f1f1f1;
            border-radius: 10px;
        }
        .chat-bubble {
            padding: 10px;
            border-radius: 10px;
            font-size: 1em;
            max-width: 70%;
            word-wrap: break-word;
            border: 1px solid #CCC;
            margin-bottom: 10px;
        }
        .chat-bubble.user {
            background-color: #DCF8C6;
            align-self: flex-end;
        }
        .chat-bubble.bot {
            background-color: #E1F3FB;
            align-self: flex-start;
        }
        .chat-input {
            display: flex;
            gap: 10px;
            padding: 10px;
            background-color: #fff;
            border-top: 1px solid #CCC;
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
        }
        .chat-input button {
            background-color: #075E54;
            color: white;
            border: none;
            padding: 10px;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            font-size: 1em;
            border: 1px solid #CCC;
            border-radius: 5px;
        }
    </style>
"""

# Azure Speech API and OpenAI API credentials
AZURE_SPEECH_KEY = "5b33a97d32f745e09cc5b955e4f1120e"
AZURE_SPEECH_REGION = "southeastasia"
API_KEY = 'ee663c94e2384769a782442342bf3a56'  # Paste your API key here
ENDPOINT = 'https://bobthebuilder001.openai.azure.com/'  # Your endpoint URL
DEPLOYMENT_NAME = 'gpt-35-turbo'  # Ensure this matches your deployment name

# Setup for Azure Speech-to-Text
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Function to recognize speech
def recognize_speech():
    try:
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        st.write("You can speak now. I'm listening...")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        return speech_recognition_result.text
    except Exception as e:
        st.error("Mic is not available. Please check your microphone settings.")
        return None

# Function to get chatbot response from Azure OpenAI
def get_chatbot_response(user_input):
    headers = {
        'Content-Type': 'application/json',
        'api-key': API_KEY,
    }

    # Structure the data correctly for chat models
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
    
    url = f"{ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2023-05-15"  # Updated API version
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()  # Updated parsing for response
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Function to synthesize speech
def synthesize_speech(text):
    try:
        audio_config = speechsdk.audio.AudioOutConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        return speech_synthesis_result
    except Exception as e:
        st.error("Error with speech synthesis. Please try again later.")
        return None

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("<h1 class='custom-title'>BoB The Banker</h1>", unsafe_allow_html=True)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def add_message(sender, message):
    st.session_state['chat_history'].append({'sender': sender, 'message': message})

# Button for starting voice recognition
if st.button("Start Speaking", key="start_button"):
    with st.spinner("Listening..."):
        user_input = recognize_speech()
        if user_input:
            add_message("user", user_input)
            with st.spinner("Generating response..."):
                response_text = get_chatbot_response(user_input)
                if response_text:
                    add_message("bot", response_text)
                    synthesize_speech(response_text)

# Text input for chatbot interaction
user_text = st.text_input("Type your message here...")

if st.button("Send", key="send_button"):
    if user_text:
        add_message("user", user_text)
        with st.spinner("Generating response..."):
            response_text = get_chatbot_response(user_text)
            if response_text:
                add_message("bot", response_text)
                synthesize_speech(response_text)

# Display chat history
st.markdown("<div class='chat-window'><div class='chat-history'>", unsafe_allow_html=True)
for chat in st.session_state['chat_history']:
    sender = "user" if chat['sender'] == "user" else "bot"
    st.markdown(f"<div class='chat-bubble {sender}'>{chat['message']}</div>", unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)
