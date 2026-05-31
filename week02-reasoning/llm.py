import os
from anthropic import Anthropic
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

_client = Anthropic()

_total_input_tokens = 0
_total_output_tokens = 0

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call(
    prompt: str,
    system: str = None,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    model: str = "claude-sonnet-4-5",
) -> str:

    global _total_input_tokens, _total_output_tokens

    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": prompt}],
    }

    if system:
        kwargs["system"] = system

    response = _client.messages.create(**kwargs)

    _total_input_tokens += response.usage.input_tokens
    _total_output_tokens += response.usage.output_tokens

    return response.content[0].text.strip()

def get_usage():
    return {
        "input_tokens": _total_input_tokens,
        "output_tokens": _total_output_tokens,
    }

def reset_usage():
    global _total_input_tokens, _total_output_tokens
    _total_input_tokens = 0
    _total_output_tokens = 0