
import requests

API_KEY = ""  
url = "https://api.groq.com/openai/v1/chat/completions"  

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "mixtral-8x7b-32768",  
    "messages": [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

response = requests.post(url, json=data, headers=headers)

print(response.json()) 
