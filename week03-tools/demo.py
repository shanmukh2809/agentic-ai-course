"""
Stress test suite - 5 challenging queries.
"""
from agent import run_agent

QUERIES = [
    "If Tokyo's population doubled and Toronto's stayed the same, what would the ratio be?",
    "What's the weather like?",
    "What's the current Bitcoin price?",
    "How many vowels are in 'unconscientiousness'?",
    "Calculate (47832 * 91245) - (12345 * 67890), then tell me how many digits the result has.",
]

def main():
    for i, q in enumerate(QUERIES, 1):
        print(f"\n{'#'*70}")
        print(f"# Query {i}: {q}")
        print(f"{'#'*70}")
        result = run_agent(q, verbose=True, max_iters=8)
        print(f"\n>>> FINAL: {result['final_text']}")
        print(f">>> Stats: {result['iterations']} iters, {len(result['tool_calls'])} tool calls, stopped: {result['stopped_due_to']}")

if __name__ == "__main__":
    main()