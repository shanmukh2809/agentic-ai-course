import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "anthropic/claude-haiku-4-5",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": "In exactly 3 sentences, explain what an AI agent is."
            }
        ]
    }
)

data = response.json()
reply = data["choices"][0]["message"]["content"]
input_tokens = data["usage"]["prompt_tokens"]
output_tokens = data["usage"]["completion_tokens"]

print("Claude says:\n")
print(reply)
print(f"\nTokens used — Input: {input_tokens}, Output: {output_tokens}")