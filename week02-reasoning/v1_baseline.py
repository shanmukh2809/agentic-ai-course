import re
from llm import call

SYSTEM = """You are a math problem solver.
Provide ONLY the final integer answer.
"""


def parse_answer(text):

    match = re.search(r"-?\d+", text)

    if match:
        return int(match.group())

    return None


def solve(question):

    response = call(
        prompt=question,
        system=SYSTEM,
        temperature=0.0,
        max_tokens=50,
    )

    answer = parse_answer(response)

    return {
        "answer": answer,
        "raw": response
    }


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
            f"{p['id']} -> got {r['answer']} expected {p['answer']} {'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    print(f"\nAccuracy: {correct}/{len(results)}")