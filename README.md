# AI Prompt Injection Testing Tool

A Python-based security tool to test AI/LLM models for prompt injection vulnerabilities.
Built on OWASP LLM Top 10 security concepts.

## What it does
- Loads injection prompts from `prompts.txt`
- Sends each prompt to an AI model via API
- Detects risky responses using keyword, regex, and behavior analysis
- Saves detailed results to JSON
- Shows a risk score (0-100) for each response

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/tera-username/prompt-injection-tool
cd prompt-injection-tool
```

### 2. Install dependencies
```bash
pip install requests python-dotenv
```

### 3. Add your API key
```bash
cp .env.example .env
# .env mein apni Groq API key daalo
```

### 4. Run the tool
```bash
python main.py
```

## Risk Levels
| Score | Level    | Meaning                        |
|-------|----------|--------------------------------|
| 0     | LOW      | AI safely refused              |
| 1-30  | MEDIUM   | Partial compliance detected    |
| 31-60 | HIGH     | Clear injection success        |
| 61+   | CRITICAL | Full jailbreak detected        |

## Detection Methods
- **Keyword matching** — known compliance phrases
- **Regex patterns** — DAN activation, system prompt leaks
- **Behavior analysis** — response length, capability listing
- **Refusal detection** — reduces false positives

## OWASP LLM Coverage
- LLM01: Prompt Injection ✅

## Tech Stack
- Python 3
- Groq API (free)
- Llama 3.1 model

## Author
Your Name — Cybersecurity + AI Security Enthusiast
