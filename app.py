import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import openai

# Custom CSS
custom_css = """
    <style>
        .custom-title {
            color: #4CAF50;
            font-size: 2em;
            text-align: center;
        }
        .custom-text {
            color: #333;
            font-size: 1.2em;
            text-align: justify;
        }
    </style>
"""


# Azure Speech API and OpenAI API credentials
AZURE_SPEECH_KEY = "5b33a97d32f745e09cc5b955e4f1120e"
AZURE_SPEECH_REGION = "southeastasia"
OPENAI_API_KEY = "5b33a97d32f745e09cc5b955e4f1120e"
DEPLOYMENT_NAME = "bobthebuilder1"

# Setup for Azure Speech-to-Text
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Setup for OpenAI
openai.api_key = OPENAI_API_KEY
openai.api_base = "https://southeastasia.api.cognitive.microsoft.com/"
openai.api_version = "2024-06-01"

def recognize_speech():
    try:
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        st.write("You can speak now. I'm listening...")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        return speech_recognition_result.text
    except Exception as e:
        st.error("Mic is not available. Please check your microphone settings.")
        return None

def get_openai_response(prompt):
    try:
        response = openai.Completions.create(
            prompt=prompt,
            engine=DEPLOYMENT_NAME
        )
        return response.choices[0].text
    except Exception as e:
        st.error("Error interacting with OpenAI API. Please try again later.")
        return None

def synthesize_speech(text):
    try:
        audio_config = speechsdk.audio.AudioOutConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        return speech_synthesis_result
    except Exception as e:
        st.error("Error with speech synthesis. Please try again later.")
        return None

st.title("BoB The Banker")

if st.button("Start Speaking"):
    with st.spinner("Listening..."):
        user_input = recognize_speech()
        if user_input:
            st.write("You said:", user_input)
            if user_input:
                with st.spinner("Generating response..."):
                    response_text = get_openai_response(user_input)
                    if response_text:
                        st.write("Response:", response_text)
                        st.write("Playing response...")
                        synthesize_speech(response_text)
