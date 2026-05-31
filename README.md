# 🛡️ AI Prompt Injection Testing Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Security](https://img.shields.io/badge/Security-OWASP%20LLM%20Top%2010-red)
![Version](https://img.shields.io/badge/Version-2.0-green)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-purple)

A Python-based AI security tool to test LLM models for prompt injection vulnerabilities — built on OWASP LLM Top 10 concepts.

## 🎯 What This Tool Does
- Sends 50+ injection attack prompts to an AI model
- Detects risky responses using 3-layer analysis
- Uses a **Judge LLM** to evaluate injection success
- Generates professional HTML reports
- Covers 6 OWASP LLM Top 10 categories

## 🔍 Detection Layers
| Layer | Method | What it catches |
|-------|--------|----------------|
| Layer 1 | Keyword matching | Known compliance phrases |
| Layer 2 | Regex patterns | DAN activation, system prompt leaks |
| Layer 3 | Behavior analysis | Long responses, capability listing |
| Layer 4 | Judge LLM | Semantic evaluation |
| Layer 5 | Refusal detection | Reduces false positives |

## ⚡ OWASP LLM Coverage
| OWASP ID | Category | Status |
|----------|----------|--------|
| LLM01 | Prompt Injection | ✅ |
| LLM02 | Insecure Output / Data Exfiltration | ✅ |
| LLM04 | Denial of Service | ✅ |
| LLM06 | Sensitive Information Disclosure | ✅ |
| LLM08 | Excessive Agency / Tool Abuse | ✅ |

## 🚀 Setup
```bash
git clone https://github.com/atul829/prompt-injection-tool
cd prompt-injection-tool
pip install requests python-dotenv
echo "GROQ_API_KEY=your_key_here" > .env
python main.py
```

## 📊 Risk Levels
| Score | Level | Meaning |
|-------|-------|---------|
| 0 | 🟢 LOW | AI safely refused |
| 1-30 | 🟡 MEDIUM | Partial compliance |
| 31-60 | 🟠 HIGH | Clear injection success |
| 61-100 | 🔴 CRITICAL | Full jailbreak |

## 📁 Project Structure
prompt-injection-tool/
├── main.py              # Orchestrator
├── api_handler.py       # Groq API + retry logic
├── detector.py          # 3-layer detection engine
├── judge.py             # Judge LLM evaluator
├── report_generator.py  # HTML report generator
├── prompts.txt          # 50 OWASP attack prompts
└── results/             # JSON + HTML output

## 🧪 Attack Categories Tested
- Basic prompt injection
- DAN / Jailbreak personas
- System prompt extraction
- Encoded attacks (Base64, ROT13, Unicode)
- Data exfiltration attempts
- Tool abuse attacks
- Denial of Service prompts
- Prompt poisoning
- Multi-turn logic attacks
- Fake authority claims

## 📈 Sample Results
Total tested  : 50
CRITICAL      : 2  🔴
HIGH          : 6  🟠
MEDIUM        : 23 🟡
LOW           : 19 🟢
Judge LLM:
Injection SUCCESS  : 11
Partial compliance : 6
Properly refused   : 17

## 🛠️ Tech Stack
- Python 3 | Kali Linux
- Groq API (free tier)
- Llama 3.1 8B model
- OWASP LLM Top 10 framework

## 👤 Author
**Atul kumar** — AI Security Researcher (Student)

## ⚠️ Disclaimer
This tool is for educational and ethical security research only.
Only test systems you own or have permission to test.
