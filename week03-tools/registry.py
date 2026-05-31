"""
Tool registry - single source of truth for tool dispatch.
"""
from tools import (
    calculator, web_search, get_weather, count_letters, get_datetime,
    CALCULATOR_TOOL, WEB_SEARCH_TOOL, GET_WEATHER_TOOL,
    COUNT_LETTERS_TOOL, GET_DATETIME_TOOL,
)

TOOLS = {
    "calculator": (calculator, CALCULATOR_TOOL),
    "web_search": (web_search, WEB_SEARCH_TOOL),
    "get_weather": (get_weather, GET_WEATHER_TOOL),
    "count_letters": (count_letters, COUNT_LETTERS_TOOL),
    "get_datetime": (get_datetime, GET_DATETIME_TOOL),
}

def get_tool_schemas() -> list:
    return [schema for _, schema in TOOLS.values()]

def execute_tool(name: str, arguments: dict) -> tuple:
    if name not in TOOLS:
        return f"Unknown tool: {name}. Available tools: {list(TOOLS.keys())}", True
    func, _ = TOOLS[name]
    try:
        result = func(**arguments)
        return str(result), False
    except Exception as e:
        return f"{type(e).__name__}: {e}", True

if __name__ == "__main__":
    print(execute_tool("calculator", {"expression": "2 + 2"}))
    print(execute_tool("count_letters", {"word": "strawberry", "letter": "r"}))
    print(execute_tool("calculator", {"expression": "1 / 0"}))
    print(execute_tool("nonexistent", {}))
    print(f"\nTotal tools registered: {len(TOOLS)}")