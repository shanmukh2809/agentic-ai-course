# Week 1 Lab Reflection

## 1. What surprised you about working with LLM APIs?

The most surprising part was how simple the API call structure is.
Just a model name, messages array, and parameters — and you get
intelligent responses instantly. The simplicity hides incredible complexity underneath.

## 2. What was the most confusing part? How did you resolve it?

Managing API keys securely was initially confusing. I resolved it
by using the python-dotenv library to load keys from a .env file,
and added .env to .gitignore to prevent accidental commits.

## 3. Temperature comparison — which was most useful?

Temperature 0.0 produced consistent, focused outputs — best for
factual tasks. Temperature 0.7 gave natural variation while staying
coherent — ideal for most agent tasks. Temperature 1.0 was highly
creative but sometimes too random to be useful. For this course,
0.7 seems like the sweet spot for agentic tasks.

## 4. One question about agentic AI after this lab?

How do real-world agents decide when to stop reasoning and take
action? In our hello_agent.py, the loop is controlled by the user,
but autonomous agents must make that decision themselves — what
mechanisms govern that boundary?
