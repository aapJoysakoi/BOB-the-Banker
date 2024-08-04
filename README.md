# BoB The Banker

BoB The Banker is a web application designed to enhance customer service in the banking sector using Azure Cognitive Services for speech-to-text and speech synthesis, and Azure OpenAI for chatbot functionality. The application allows users to interact with a virtual banking assistant via text and voice inputs, receiving intelligent responses to their queries.

### Features

- **Speech Recognition**: Convert user speech to text using Azure Cognitive Services.
- **Chatbot Integration**: Communicate with a chatbot powered by Azure OpenAI.
- **Speech Synthesis**: Convert chatbot responses to speech for auditory feedback.
- **Responsive UI**: User-friendly interface for seamless interactions.

### Chat Interface :

![image](https://github.com/user-attachments/assets/7ac29550-9042-493e-952a-a1430ff413c5)


### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/aapJoysakoi/BOB-the-Banker.git
   cd BOB-the-Banker
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add the following environment variables:
     ```plaintext
     AZURE_SPEECH_KEY=your_azure_speech_key
     AZURE_SPEECH_REGION=your_azure_speech_region
     API_KEY=your_azure_openai_api_key
     ENDPOINT=your_azure_openai_endpoint
     DEPLOYMENT_NAME=your_openai_deployment_name
     ```

### Running the Application

1. **Start the Flask App**
   ```bash
   flask run
   ```

2. **Access the Application**
   - Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Usage

1. **Text Interaction**
   - Type your message in the input box and click the "Send" button or press Enter.
   - The chatbot will respond, and the response will be displayed in the chat window.

2. **Voice Interaction**
   - Click the microphone button to start speech recognition.
   - Speak your query, and the recognized text will be sent to the chatbot.
   - The chatbot's response will be converted to speech and played back to you.

### Dependencies

- Flask
- azure-cognitiveservices-speech
- requests

### License

This project is licensed under the MIT License.
