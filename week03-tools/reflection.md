# Week 3 Lab Reflection

## 1. Which Week 2 failures became trivial with tools?

All arithmetic problems became trivial with the calculator tool.
Big multiplication like 47832 \* 91245 which the LLM got wrong before,
now succeeds perfectly. Character counting with count_letters also
fixed the strawberry problem completely. Real-time facts via web_search
solved the Tokyo/Toronto population query instantly.

## 2. Most surprising agent behavior in stress tests?

The most surprising behavior was when asked about Bitcoin price —
the agent cleanly admitted it had no tool for that instead of
hallucinating an answer. It showed the agent knows its own limitations.
Also impressive was multi-tool chaining where it called web_search
twice then calculator automatically without any guidance.

## 3. How many tool calls did the longest query take?

The longest query (calculate difference then count digits) took
3 tool calls: one for the first multiplication, one for the second,
and one for the subtraction. In production this means 3x API latency
and cost per complex query, which needs careful optimization.

## 4. What would you change in DEFAULT_SYSTEM prompt?

I would add explicit instructions like "always use count_letters for
any letter counting task, never try to count yourself" and "if no
tool exists for a query, say so clearly rather than guessing." This
would reduce hallucination and improve reliability significantly.

## 5. Complementary tool idea?

For the calculator tool, I would add a unit_converter tool that
converts between units like km to miles, celsius to fahrenheit, etc.
These two tools together would handle almost all quantitative
questions a user might ask in everyday scenarios.
