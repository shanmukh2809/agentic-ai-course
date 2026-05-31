import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY")
print("API Key Status:")
print(f"  OpenRouter: {'Found' if key else 'Missing'}")
if key:
    print(f"  Key prefix: {key[:15]}...")