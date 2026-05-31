"""
v2: Zero-shot CoT
"""

import re
from llm import call

SYSTEM = """You are a careful math problem solver.

For every problem:
1. Reason step by step inside <reasoning>...</reasoning>
2. Give final answer inside <answer>...</answer>

Always show reasoning.
"""


def solve(question: str):

    response = call(
        prompt=question,
        system=SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    answer = parse_answer(response)

    return {
        "answer": answer,
        "raw": response,
    }


def parse_answer(text: str):

    match = re.search(
        r"<answer>\s*(-?\d[\d,]*)\s*</answer>",
        text,
        re.IGNORECASE,
    )

    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except:
            return None

    nums = re.findall(r"-?\d+", text.replace(",", ""))

    return int(nums[-1]) if nums else None


def run_all():

    from problems import get_problems

    results = []

    for p in get_problems():

        r = solve(p["question"])

        correct = r["answer"] == p["answer"]

        results.append({
            "id": p["id"],
            "difficulty": p["difficulty"],
            "expected": p["answer"],
            "got": r["answer"],
            "correct": correct,
        })

        print(
            f"{p['id']} ({p['difficulty']}): "
            f"got {r['answer']} expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":

    print("=== v2 Zero Shot CoT ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(f"\nAccuracy: {correct}/{len(results)}")