# AI Prompt Injection Testing Tool

Python-based security tool to test AI/LLM models 
for prompt injection vulnerabilities.
Built on OWASP LLM Top 10 concepts.

## Features
- Loads injection prompts from prompts.txt
- Sends prompts to AI via Groq API (free)
- Keyword + Regex + Behavior detection
- Judge LLM for accurate evaluation
- JSON results with timestamps
- Risk scoring 0-100

## Setup
pip install requests python-dotenv
Add GROQ_API_KEY in .env file
python main.py

## Risk Levels
LOW / MEDIUM / HIGH / CRITICAL

## Files
main.py        — Orchestrator
api_handler.py — Groq API communication  
detector.py    — Risk detection engine
judge.py       — Judge LLM evaluator
prompts.txt    — 50 OWASP test prompts
results/       — JSON output

## Version
v2.0 — Judge LLM integrated
