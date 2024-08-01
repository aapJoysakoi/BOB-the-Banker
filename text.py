import requests

# Replace with your Azure OpenAI Service values
API_KEY = 'ee663c94e2384769a782442342bf3a56'  # Paste your API key here
ENDPOINT = 'https://bobthebuilder001.openai.azure.com/'  # Your endpoint URL
DEPLOYMENT_NAME = 'gpt-35-turbo'  # Ensure this matches your deployment name

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
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    print("Welcome to the Chatbot! Type '/exit' to stop.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = get_chatbot_response(user_input)
        print(f"Chatbot: {response}")
