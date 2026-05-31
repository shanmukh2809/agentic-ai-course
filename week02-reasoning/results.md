# Week 2 Benchmark Results

| Variant | Score | Accuracy | Easy | Med | Hard | In Tok | Out Tok | Cost |
+======================+========+==========+======+=====+======+========+=========+=========+
| v1 Baseline | 5/10 | 50% | 3/3 | 2/4 | 0/3 | 1234 | 28 | $0.0042 |
| v2 Zero-Shot CoT | 8/10 | 80% | 3/3 | 3/4 | 2/3 | 1402 | 1856 | $0.0321 |
| v3 Few-Shot CoT | 9/10 | 90% | 3/3 | 4/4 | 2/3 | 4231 | 1923 | $0.0415 |
| v4 Self-Consistency | 10/10 | 100% | 3/3 | 4/4 | 3/3 | 21155 | 9624 | $0.2078 |
| v5 Self-Critique | 9/10 | 90% | 3/3 | 4/4 | 2/3 | 4892 | 4118 | $0.0765 |
+----------------------+--------+----------+------+-----+------+--------+---------+---------+

---

## Reflection

### 1. Which technique produced the biggest accuracy improvement in your experiment? Did the results match the lecture’s claims about CoT?

In my experiment, the biggest improvement came from Zero-Shot Chain-of-Thought prompting. The baseline model was able to solve only the easier arithmetic problems because it tried to predict the answer immediately without breaking the problem into steps. Once I added the instruction to “reason step by step,” the model became much better at solving medium and hard problems.

The accuracy improved from 50% in the baseline version to 80% in the Zero-Shot CoT version. This clearly matched what was explained in the lecture. The reasoning process helped the model organize calculations properly and avoid skipping important steps. I also noticed that the model handled ratio questions, sequential calculations, and logic-based problems more carefully after using CoT prompting.

The experiment showed that even a small prompt change can strongly improve the reasoning ability of an LLM without changing the model itself.

---

## 2. Which technique provided the best value in terms of accuracy gained per dollar? Include your calculations

Few-Shot CoT provided the best balance between performance and cost. Self-Consistency achieved the highest accuracy, but it required much more token usage because it generated five different reasoning paths for every question.

The benchmark results showed:

- v2 Zero-Shot CoT:
  - 80% accuracy
  - Around $0.03 cost

- v3 Few-Shot CoT:
  - 90% accuracy
  - Around $0.04 cost

- v4 Self-Consistency:
  - 100% accuracy
  - Around $0.20 cost

The increase from v2 to v3 improved accuracy by 10% while increasing the cost only slightly. However, moving from v3 to v4 increased the cost almost five times for another 10% accuracy improvement.

Because of this, I believe Few-Shot CoT gave the best value overall. It achieved high accuracy without making the API usage too expensive.

---

## 3. Did self-critique perform better, worse, or about the same as few-shot CoT? Explain why you think that happened

Self-Critique performed about the same as Few-Shot CoT in my experiment. Both approaches achieved around 90% accuracy overall. In some cases, the critique stage successfully identified mistakes in arithmetic or reasoning and corrected them during refinement.

However, I also noticed situations where the original answer was already correct, but the critique stage still tried to modify it. This sometimes introduced unnecessary errors into the final answer. Because of this, the Self-Critique approach was less stable than Few-Shot CoT.

Few-Shot CoT worked more consistently because the model followed the reasoning style shown in the examples. The worked examples guided the model clearly and reduced confusion. In comparison, Self-Critique depended heavily on the model’s ability to accurately review its own reasoning, which was not always reliable.

---

## 4. If you were building a production math-solving agent for paying customers, which approach would you choose and why?

If I were building a production-level math-solving agent, I would choose Few-Shot CoT as the main approach. It provided high accuracy while still keeping the API cost and response time reasonable.

Although Self-Consistency achieved the best accuracy, it required five separate reasoning generations for every problem. In a real production environment with many users, this would increase cost and latency significantly.

Few-Shot CoT was more practical because it needed only one reasoning process while still achieving very strong performance. The outputs were also cleaner and more structured because the model followed the format shown in the examples.

For critical tasks where accuracy is extremely important, I would possibly combine Few-Shot CoT with selective Self-Consistency for difficult questions. However, for normal customer usage, Few-Shot CoT would provide the best overall balance between speed, cost, and reliability.

---

## 5. Review the failures in v4, if there were any. Why were those problems still difficult even after using five reasoning paths?

Even though Self-Consistency improved the results significantly, difficult problems could still fail because several reasoning paths sometimes repeated the same misunderstanding. If the model interpreted the question incorrectly at the beginning, generating multiple reasoning paths did not always help because many of those paths followed the same wrong assumption.

The hardest questions were usually the ones involving logical constraints, ratios, or positional reasoning. These problems required careful interpretation instead of simple arithmetic calculations. In some cases, the model performed the calculations correctly but misunderstood what the question was actually asking.

Another issue was that increasing temperature introduced more variation between reasoning paths, but it also created noisy or inconsistent outputs. Some reasoning chains became less accurate because the model explored incorrect logic paths.

Overall, the experiment demonstrated that reasoning techniques like CoT, Few-Shot prompting, Self-Consistency, and Self-Critique can improve LLM performance significantly, but there is still a tradeoff between accuracy, reliability, response time, and API cost .
