import os
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
console = Console()

SYSTEM_PROMPT = """You are a friendly and concise AI study buddy for a student
learning about Agentic AI. Keep responses under 4 sentences unless asked for
more detail. Use simple analogies when explaining technical concepts."""

conversation_history = []

def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "anthropic/claude-haiku-4-5",
            "max_tokens": 1024,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        }
    )

    assistant_message = response.json()["choices"][0]["message"]["content"]

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

def main():
    console.print(Panel.fit(
        "[bold cyan]Hello Agent[/bold cyan]\n"
        "Your AI study buddy for Agentic AI.\n"
        "[dim]Type 'quit' or 'exit' to end the conversation.[/dim]",
        border_style="cyan"
    ))

    while True:
        user_input = Prompt.ask("\n[bold green]You[/bold green]")

        if user_input.lower() in ["quit", "exit", "bye"]:
            console.print("\n[yellow]Goodbye! Happy learning![/yellow]")
            break

        try:
            response = chat(user_input)
            console.print(f"\n[bold magenta]Agent[/bold magenta]: {response}")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            break

    console.print(f"\n[dim]Total exchanges: {len(conversation_history) // 2}[/dim]")

if __name__ == "__main__":
    main()