import os
from azure import cognitiveservices

AZURE_SPEECH_KEY = "5b33a97d32f745e09cc5b955e4f1120e"
AZURE_SPEECH_REGION = "southeastasia"
speech_config = azure.cognitiveservices.speech.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
speech_config.speech_recognition_language = "en-US"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
print("You can speak now. I'm listening...")
speech_recognition_result = speech_recognizer.recognize_once_async().get()
output = speech_recognition_result.text
print(output)
deployment_name= "bobthebuilder1"
openai.api_type="azure"
openai.api_key="5b33a97d32f745e09cc5b955e4f1120e"
openai.api_base ="https://southeastasia.api.cognitive.microsoft.com/"
openai.api_version="2024-06-01"
deployment_name= "bobthebuilder1"
response = openai.Completions.create(prompt=output,engine=deployment_name)
output = response.choices[0].text
print(output)
audio_config = speechsdk.audio.AudioOutConfig(use_default_speaker=True)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
speech_synthesis_result = speech_synthesizer.speak_text_async(output).get()