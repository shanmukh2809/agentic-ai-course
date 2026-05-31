"""
Five tools for our agent. Each tool is a function + a JSON schema.
"""
import datetime
import math
import re

def calculator(expression: str) -> str:
    if not re.match(r'^[\d\s\+\-\*\/\.\(\)\,\^a-zA-Z_]+$', expression):
        raise ValueError(f"Expression contains disallowed characters: {expression}")
    safe_globals = {
        "__builtins__": {},
        "abs": abs, "round": round, "min": min, "max": max,
        "math": math,
    }
    try:
        result = eval(expression, safe_globals)
        return str(result)
    except Exception as e:
        raise ValueError(f"Could not evaluate '{expression}': {e}")

CALCULATOR_TOOL = {
    "name": "calculator",
    "description": "Evaluate a math expression. Use for any precise arithmetic. Use Python syntax: '47832 * 91245', 'round(13.96 / 2.93)', '2**10'.",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "A Python-syntax math expression."
            }
        },
        "required": ["expression"]
    }
}

_WEB_FACTS = {
    "tokyo population": "Tokyo's population is approximately 13.96 million (2023 estimate).",
    "toronto population": "Toronto's population is approximately 2.93 million (2023 estimate).",
    "paris population": "Paris's population is approximately 2.16 million (2023 estimate).",
    "speed of light": "The speed of light in vacuum is 299,792,458 m/s.",
    "boiling point of water": "Water boils at 100°C (212°F) at standard atmospheric pressure.",
    "moon distance": "The Moon is approximately 384,400 km from Earth on average.",
}

def web_search(query: str) -> str:
    query_lower = query.lower()
    for key, value in _WEB_FACTS.items():
        if all(word in query_lower for word in key.split()):
            return value
    return f"No relevant results found for '{query}'. Try a different query."

WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the public web for current factual information like population data, scientific constants, geographic facts.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A concise search query, 2-6 words."
            }
        },
        "required": ["query"]
    }
}

_WEATHER_DATA = {
    "toronto": {"temp_c": 14, "conditions": "partly cloudy"},
    "tokyo": {"temp_c": 22, "conditions": "sunny"},
    "london": {"temp_c": 11, "conditions": "rainy"},
    "paris": {"temp_c": 16, "conditions": "cloudy"},
    "sydney": {"temp_c": 25, "conditions": "clear"},
}

def get_weather(location: str) -> dict:
    key = location.lower().strip()
    if key not in _WEATHER_DATA:
        raise ValueError(f"Weather not available for '{location}'. Try: Toronto, Tokyo, London, Paris, Sydney.")
    return {"location": location, **_WEATHER_DATA[key]}

GET_WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get current weather for a city. Returns temperature in Celsius and conditions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "A city name. E.g., 'Toronto', 'Tokyo', 'London'."
            }
        },
        "required": ["location"]
    }
}

def count_letters(word: str, letter: str) -> int:
    if len(letter) != 1:
        raise ValueError(f"'letter' must be a single character, got: '{letter}'")
    return word.lower().count(letter.lower())

COUNT_LETTERS_TOOL = {
    "name": "count_letters",
    "description": "Count occurrences of a specific letter in a word or string.",
    "input_schema": {
        "type": "object",
        "properties": {
            "word": {"type": "string", "description": "The word or string to search in."},
            "letter": {"type": "string", "description": "Single letter to count. Case-insensitive."}
        },
        "required": ["word", "letter"]
    }
}

# === Tool 5: Get Datetime ===
def get_datetime() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")

GET_DATETIME_TOOL = {
    "name": "get_datetime",
    "description": "Get the current date and time.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

if __name__ == "__main__":
    print(calculator("47832 * 91245"))
    print(web_search("Tokyo population"))
    print(get_weather("Toronto"))
    print(count_letters("strawberry", "r"))
    print(get_datetime())