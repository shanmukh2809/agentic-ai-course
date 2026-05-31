"""
v5: Self Critique
Generate -> Critique -> Refine
"""

import re
from llm import call

GENERATE_SYSTEM = """
You are a math problem solver.

Reason step by step inside <reasoning>...</reasoning>

Then provide final answer inside <answer>...</answer>
"""

CRITIQUE_SYSTEM = """
You are a meticulous math reviewer.

Check:
- Setup
- Arithmetic
- Logic
- Final answer

Reply exactly in this format:

<issues>
List issues or say:
None — solution looks correct.
</issues>

<verdict>correct or incorrect</verdict>
"""

REFINE_SYSTEM = """
You are revising your previous answer.

Use the critique feedback to improve the solution.

Reason step by step inside <reasoning>...</reasoning>

Then provide final answer inside <answer>...</answer>
"""


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


def parse_verdict(text: str):

    match = re.search(
        r"<verdict>\s*(\w+)\s*</verdict>",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).lower()

    return "unknown"


def solve(question: str):

    # Step 1 Generate

    initial = call(
        prompt=question,
        system=GENERATE_SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    # Step 2 Critique

    critique_prompt = (
        f"Problem: {question}\n\n"
        f"Proposed solution:\n{initial}\n\n"
        f"Review carefully."
    )

    critique = call(
        prompt=critique_prompt,
        system=CRITIQUE_SYSTEM,
        temperature=0.0,
        max_tokens=512,
    )

    verdict = parse_verdict(critique)

    # If correct return initial

    if verdict == "correct":

        return {
            "answer": parse_answer(initial),
            "iterations": 1,
            "verdict": verdict,
        }

    # Step 3 Refine

    refine_prompt = (
        f"Problem: {question}\n\n"
        f"Previous solution:\n{initial}\n\n"
        f"Review feedback:\n{critique}\n\n"
        f"Now revise solution."
    )

    refined = call(
        prompt=refine_prompt,
        system=REFINE_SYSTEM,
        temperature=0.0,
        max_tokens=1024,
    )

    return {
        "answer": parse_answer(refined),
        "iterations": 2,
        "verdict": verdict,
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
            "iterations": r["iterations"],
        })

        print(
            f"{p['id']} ({p['difficulty']}): "
            f"got {r['answer']} "
            f"(iters={r['iterations']}, verdict={r['verdict']}) "
            f"expected {p['answer']} "
            f"{'OK' if correct else 'FAIL'}"
        )

    return results


if __name__ == "__main__":

    print("=== v5 Self Critique ===")

    results = run_all()

    correct = sum(1 for r in results if r["correct"])

    refined_count = sum(
        1 for r in results if r["iterations"] > 1
    )

    print(f"\nAccuracy: {correct}/{len(results)}")

    print(
        f"Refined problems: "
        f"{refined_count}/{len(results)}"
    )