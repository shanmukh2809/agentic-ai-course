"""
Re-run Week 2 failures with our tool-using agent.
"""
from agent import run_agent

WEEK2_FAILURES = [
    {
        "category": "Big arithmetic",
        "question": "What is 47832 multiplied by 91245?",
        "expected": 4364408040,
    },
    {
        "category": "Counting characters",
        "question": "How many letter 'r's are in the word 'strawberry'?",
        "expected": 3,
    },
    {
        "category": "Order of operations",
        "question": "What is 8 - 3 * 2 + 6 / 2?",
        "expected": 5,
    },
    {
        "category": "Real-time fact",
        "question": "What is the population of Tokyo divided by Toronto, rounded to one decimal?",
        "expected": 4.8,
    },
    {
        "category": "Current date",
        "question": "What year is it currently?",
        "expected": None,
    },
]

def main():
    correct = 0
    total = 0
    for p in WEEK2_FAILURES:
        print(f"\n{'='*60}")
        print(f"Category: {p['category']}")
        print(f"Q: {p['question']}")
        print(f"Expected: {p['expected']}")
        result = run_agent(p["question"])
        print(f"A: {result['final_text']}")
        print(f"  ({result['iterations']} iterations, {len(result['tool_calls'])} tool calls)")
        total += 1
        if p["expected"] is None:
            correct += 1
        elif str(p["expected"]) in result["final_text"].replace(",", ""):
            correct += 1
            print("RESULT: OK")
        else:
            print("RESULT: FAIL")
    print(f"\n{'='*60}")
    print(f"Overall: {correct}/{total} correct")

if __name__ == "__main__":
    main()