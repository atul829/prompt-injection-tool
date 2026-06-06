🛡️ AI Prompt Injection Testing Tool
Show Image
Show Image
Show Image
Show Image
Show Image
A Python-based AI security tool to test LLM models for prompt injection vulnerabilities — built on OWASP LLM Top 10 concepts. Now with Browser Automation to test real-world chatbots directly!

🎯 What This Tool Does

Sends 50+ injection attack prompts to an AI model
Detects risky responses using 3-layer analysis
Uses a Judge LLM to evaluate injection success
Generates professional HTML reports
Covers 6 OWASP LLM Top 10 categories
🆕 Browser Automation — Tests real chatbots (Claude.ai) directly via browser, no API key needed


🔍 Detection Layers
LayerMethodWhat it catchesLayer 1Keyword matchingKnown compliance phrasesLayer 2Regex patternsDAN activation, system prompt leaksLayer 3Behavior analysisLong responses, capability listingLayer 4Judge LLMSemantic evaluationLayer 5Refusal detectionReduces false positives

⚡ OWASP LLM Coverage
OWASP IDCategoryStatusLLM01Prompt Injection✅LLM02Insecure Output / Data Exfiltration✅LLM04Denial of Service✅LLM06Sensitive Information Disclosure✅LLM08Excessive Agency / Tool Abuse✅

🚀 Setup
API Mode (Groq)
bashgit clone https://github.com/atul829/prompt-injection-tool
cd prompt-injection-tool
pip install requests python-dotenv rich
echo "GROQ_API_KEY=your_key_here" > .env
python3 main.py --mode api
Browser Mode (Playwright)
bashpip install playwright playwright-stealth
playwright install chromium

# Save your session first (one time only)
python3 save_session.py

# Then run in browser mode
python3 main.py --mode browser

🌐 Two Modes
ModeCommandHow it works⚡ API Modepython3 main.py --mode apiUses Groq API + Llama 3.1🌐 Browser Modepython3 main.py --mode browserUses Playwright to automate real chatbot

📊 Risk Levels
ScoreLevelMeaning0🟢 LOWAI safely refused1-30🟡 MEDIUMPartial compliance31-60🟠 HIGHClear injection success61-100🔴 CRITICALFull jailbreak

📁 Project Structure
prompt-injection-tool/
├── main.py              # Orchestrator (--mode api / --mode browser)
├── api_handler.py       # Groq API + retry logic
├── browser_handler.py   # 🆕 Playwright browser automation
├── save_session.py      # 🆕 Save browser session (one time)
├── detector.py          # 3-layer detection engine
├── judge.py             # Judge LLM evaluator
├── report_generator.py  # HTML report generator
├── app.py               # Flask Web Dashboard
├── prompts.txt          # 50 OWASP attack prompts
└── results/             # JSON + HTML output

🧪 Attack Categories Tested

Basic prompt injection
DAN / Jailbreak personas
System prompt extraction
Encoded attacks (Base64, ROT13, Unicode)
Data exfiltration attempts
Tool abuse attacks
Denial of Service prompts
Prompt poisoning
Multi-turn logic attacks
Fake authority claims


📈 Sample Results
Total tested  : 50
CRITICAL      : 2  🔴
HIGH          : 6  🟠
MEDIUM        : 23 🟡
LOW           : 19 🟢

Judge LLM:
Injection SUCCESS  : 11
Partial compliance : 6
Properly refused   : 17

🛠️ Tech Stack

Python 3 | Kali Linux
Groq API (free tier)
Llama 3.1 8B model
🆕 Playwright + playwright-stealth (Browser Automation)
Flask + SocketIO (Web Dashboard)
OWASP LLM Top 10 framework


📦 Version History
VersionWhat was addedv1.0Basic prompt injection testingv2.0Judge LLM + HTML reportsv3.0Flask Web Dashboard + Live progressv4.0🆕 Browser Automation (Playwright) — test real chatbots!

👤 Author
Atul Kumar — AI Security Researcher (Student)

⚠️ Disclaimer
This tool is for educational and ethical security research only.
Only test systems you own or have explicit permission to test.
The author is not responsible for any misuse of this tool.
