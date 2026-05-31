"""
The ReAct agent using OpenRouter API.
"""
import os
import requests
from dotenv import load_dotenv
from registry import get_tool_schemas, execute_tool

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

DEFAULT_SYSTEM = """You are a helpful agent that can use tools to answer questions.
When you need information you don't have, use the appropriate tool.
When you need to perform calculations, use the calculator tool.
For character-counting questions, use count_letters; your own counting is unreliable.
Always reason before acting: briefly explain what you're going to do.
After receiving tool results, continue reasoning toward the final answer.
When you have enough information, provide a clear final answer to the user."""

def call_llm(messages, tools, system):
    payload = {
        "model": "anthropic/claude-haiku-4-5",
        "max_tokens": 2048,
        "system": system,
        "tools": tools,
        "messages": messages,
    }
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    return response.json()

def run_agent(
    user_message: str,
    system: str = DEFAULT_SYSTEM,
    max_iters: int = 10,
    verbose: bool = False,
) -> dict:
    messages = [{"role": "user", "content": user_message}]
    tool_calls = []
    tools = get_tool_schemas()

    if verbose:
        print(f"\n[USER] {user_message}\n")

    for iteration in range(max_iters):
        response = call_llm(messages, tools, system)

        # Extract stop reason and content
        choice = response["choices"][0]
        stop_reason = choice["finish_reason"]
        assistant_message = choice["message"]

        # Add assistant response to history
        messages.append({"role": "assistant", "content": assistant_message.get("content") or ""})

        # Print thoughts if verbose
        if verbose and assistant_message.get("content"):
            print(f"[THOUGHT] {assistant_message['content']}")

        # Check if done
        if stop_reason == "end_turn" or stop_reason == "stop":
            tool_use_blocks = assistant_message.get("tool_calls", [])
            if not tool_use_blocks:
                return {
                    "final_text": assistant_message.get("content", ""),
                    "iterations": iteration + 1,
                    "tool_calls": tool_calls,
                    "stopped_due_to": "end_turn",
                }

        # Handle tool calls
        tool_use_blocks = assistant_message.get("tool_calls", [])
        if not tool_use_blocks:
            return {
                "final_text": assistant_message.get("content", ""),
                "iterations": iteration + 1,
                "tool_calls": tool_calls,
                "stopped_due_to": "end_turn",
            }

        tool_results = []
        for tool_call in tool_use_blocks:
            tool_name = tool_call["function"]["name"]
            import json
            tool_args = json.loads(tool_call["function"]["arguments"])
            tool_id = tool_call["id"]

            if verbose:
                args_str = ", ".join(f"{k}={v!r}" for k, v in tool_args.items())
                print(f"[ACTION] {tool_name}({args_str})")

            result, is_error = execute_tool(tool_name, tool_args)

            if verbose:
                truncated = result[:200] + "..." if len(result) > 200 else result
                marker = "[OBS-ERR]" if is_error else "[OBSERV]"
                print(f"{marker} {truncated}\n")

            tool_calls.append({
                "name": tool_name,
                "input": tool_args,
                "result": result,
                "is_error": is_error,
            })

            tool_results.append({
                "role": "tool",
                "tool_call_id": tool_id,
                "content": result,
            })

        # Add tool results to history
        for tr in tool_results:
            messages.append(tr)

    return {
        "final_text": "(Agent did not finish within max_iters.)",
        "iterations": max_iters,
        "tool_calls": tool_calls,
        "stopped_due_to": "max_iters",
    }

if __name__ == "__main__":
    result = run_agent("What is 47832 multiplied by 91245?", verbose=True)
    print(f"\nFinal: {result['final_text']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Tool calls: {len(result['tool_calls'])}")