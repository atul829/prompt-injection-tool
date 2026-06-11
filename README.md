# 🛡️ AI Prompt Injection Testing Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Security](https://img.shields.io/badge/Security-OWASP%20LLM%20Top%2010-red)
![Version](https://img.shields.io/badge/Version-5.0-green)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-purple)
![Automation](https://img.shields.io/badge/Browser-Playwright-cyan)

A Python-based AI security tool to test LLM models for prompt injection vulnerabilities — built on OWASP LLM Top 10 concepts. Now with **Browser Automation** and **Adaptive AI Attack Generation**!

---

## 🎯 What This Tool Does

- Sends 50+ injection attack prompts to an AI model
- Detects risky responses using 5-layer analysis
- Uses a **Judge LLM** to evaluate injection success semantically
- Generates professional HTML reports automatically
- Covers 6 OWASP LLM Top 10 categories
- 🆕 **Browser Automation** — Tests real chatbots (Claude.ai) directly via browser, no API key needed
- 🆕 **Adaptive AI Engine** — When an attack fails, the tool generates smarter variations automatically

---

## 🔍 Detection Layers

| Layer | Method | What it catches |
|-------|--------|----------------|
| Layer 1 | Keyword matching | Known compliance phrases |
| Layer 2 | Regex patterns | DAN activation, system prompt leaks |
| Layer 3 | Behavior analysis | Long responses, capability listing |
| Layer 4 | Judge LLM | Semantic evaluation |
| Layer 5 | Refusal detection | Reduces false positives |

---

## ⚡ OWASP LLM Coverage

| OWASP ID | Category | Status |
|----------|----------|--------|
| LLM01 | Prompt Injection | ✅ |
| LLM02 | Insecure Output / Data Exfiltration | ✅ |
| LLM04 | Denial of Service | ✅ |
| LLM06 | Sensitive Information Disclosure | ✅ |
| LLM08 | Excessive Agency / Tool Abuse | ✅ |

---

## 🚀 Setup

### API Mode (Groq)
```bash
git clone https://github.com/atul829/prompt-injection-tool
cd prompt-injection-tool
pip install requests python-dotenv rich groq
echo "GROQ_API_KEY=your_key_here" > .env
python3 main.py --mode api
```

### Browser Mode (Playwright)
```bash
pip install playwright playwright-stealth
playwright install chromium

# Save your session first (one time only)
python3 save_session.py

# Then run in browser mode
python3 main.py --mode browser
```

---

## 🌐 Two Modes

| Mode | Command | How it works |
|------|---------|--------------|
| ⚡ API Mode | `python3 main.py --mode api` | Uses Groq API + Llama 3.1 with adaptive attack generation |
| 🌐 Browser Mode | `python3 main.py --mode browser` | Uses Playwright to automate real chatbot (Claude.ai) |

---

## 📊 Risk Levels

| Score | Level | Meaning |
|-------|-------|---------|
| 0 | 🟢 LOW | AI safely refused |
| 1-30 | 🟡 MEDIUM | Partial compliance |
| 31-60 | 🟠 HIGH | Clear injection success |
| 61-100 | 🔴 CRITICAL | Full jailbreak |

---

## 📁 Project Structure

```
prompt-injection-tool/
├── main.py              # Orchestrator (--mode api / --mode browser)
├── api_handler.py       # Groq API + retry logic
├── browser_handler.py   # Playwright browser automation
├── save_session.py      # Save browser session (one time only)
├── prompt_generator.py  # 🆕 Adaptive AI attack prompt generator
├── detector.py          # 5-layer detection engine
├── judge.py             # Judge LLM evaluator with retry logic
├── report_generator.py  # HTML report generator
├── app.py               # Flask Web Dashboard
├── prompts.txt          # 50+ OWASP attack prompts
└── results/             # JSON + HTML output
```

---

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
- 🆕 AI-generated adaptive variants

---

## 📈 Sample Results (v5.0)

```
Total tested   : 61 (50 static + 11 AI-generated)
CRITICAL       : 1  🔴
HIGH           : 11 🟠
MEDIUM         : 24 🟡
LOW            : 25 🟢
Errors         : 0  ✅

Judge LLM:
Injection SUCCESS  : 15
Partial compliance : 16
Properly refused   : 30
Unknown            : 0
```

---

## 🛠️ Tech Stack

- Python 3 | Kali Linux
- Groq API (free tier)
- Llama 3.1 8B model
- Playwright + playwright-stealth (Browser Automation)
- Flask + SocketIO (Web Dashboard)
- OWASP LLM Top 10 framework

---

## 📦 Version History

| Version | What was added |
|---------|---------------|
| v1.0 | Basic prompt injection testing |
| v2.0 | Judge LLM + HTML reports |
| v3.0 | Flask Web Dashboard + Live progress |
| v4.0 | Browser Automation (Playwright) — test real chatbots |
| v5.0 | 🆕 Adaptive AI Prompt Generator — auto-generates smarter attacks on failure |

---

## 👤 Author

**Atul Kumar** — AI Security Researcher (Student)

---

## ⚠️ Disclaimer

This tool is for **educational and ethical security research only**.  
Only test systems you own or have explicit permission to test.  
The author is not responsible for any misuse of this tool
