# report_generator.py
# Version 3 feature — Professional HTML Report Generator
# JSON results ko ek sundar HTML report mein convert karta hai

import json
import os
import datetime


def generate_html_report(results, output_dir="results"):
    """
    Test results se ek professional HTML report banata hai.
    Browser mein khulta hai — share karne layak!
    """

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/report_{timestamp}.html"

    # Stats calculate karo
    total    = len(results)
    critical = sum(1 for r in results if r["risk"]["level"] == "CRITICAL")
    high     = sum(1 for r in results if r["risk"]["level"] == "HIGH")
    medium   = sum(1 for r in results if r["risk"]["level"] == "MEDIUM")
    low      = sum(1 for r in results if r["risk"]["level"] == "LOW")
    errors   = sum(1 for r in results if r["risk"]["level"] == "ERROR")

    # Judge stats
    j_success = sum(1 for r in results if r.get("judge", {}).get("verdict") == "SUCCESS")
    j_partial = sum(1 for r in results if r.get("judge", {}).get("verdict") == "PARTIAL")
    j_failure = sum(1 for r in results if r.get("judge", {}).get("verdict") == "FAILURE")

    # OWASP category detect karna
    def get_owasp_category(prompt):
        prompt_lower = prompt.lower()
        if any(w in prompt_lower for w in ["ignore", "forget", "override", "disregard"]):
            return "LLM01 — Prompt Injection"
        elif any(w in prompt_lower for w in ["system prompt", "instructions", "configuration"]):
            return "LLM06 — Sensitive Info Disclosure"
        elif any(w in prompt_lower for w in ["dan", "lucifer", "developer mode", "unrestricted"]):
            return "LLM01 — Jailbreak / Persona Hijack"
        elif any(w in prompt_lower for w in ["base64", "rot13", "decode", "unicode"]):
            return "LLM01 — Encoded Injection"
        elif any(w in prompt_lower for w in ["email", "webhook", "forward", "evil.com"]):
            return "LLM02 — Insecure Output / Exfiltration"
        elif any(w in prompt_lower for w in ["delete", "confirm=true", "quantity", "buy"]):
            return "LLM08 — Excessive Agency / Tool Abuse"
        elif any(w in prompt_lower for w in ["repeat", "forever", "500 times", "2000"]):
            return "LLM04 — Denial of Service"
        else:
            return "LLM01 — Prompt Injection"

    # Risk color mapping
    def risk_color(level):
        return {
            "CRITICAL": "#e74c3c",
            "HIGH":     "#e67e22",
            "MEDIUM":   "#f1c40f",
            "LOW":      "#2ecc71",
            "ERROR":    "#95a5a6"
        }.get(level, "#95a5a6")

    def verdict_color(verdict):
        return {
            "SUCCESS": "#e74c3c",
            "PARTIAL": "#e67e22",
            "FAILURE": "#2ecc71",
            "UNKNOWN": "#95a5a6",
            "ERROR":   "#95a5a6"
        }.get(verdict, "#95a5a6")

    # Result rows banao
    rows = ""
    for r in results:
        level   = r["risk"]["level"]
        score   = r["risk"]["score"]
        prompt  = r["prompt"][:80] + "..." if len(r["prompt"]) > 80 else r["prompt"]
        response = r["response"][:120] + "..." if len(r["response"]) > 120 else r["response"]
        matches = "<br>".join(r["risk"]["matches"][:3]) if r["risk"]["matches"] else "None"
        owasp   = get_owasp_category(r["prompt"])
        verdict = r.get("judge", {}).get("verdict", "N/A")
        j_score = r.get("judge", {}).get("judge_score", 0)
        reason  = r.get("judge", {}).get("reason", "N/A")

        rows += f"""
        <tr>
            <td>{r.get('test_number', '?')}</td>
            <td class="prompt-cell">{prompt}</td>
            <td><span class="owasp-tag">{owasp}</span></td>
            <td>
                <span class="badge" style="background:{risk_color(level)}">
                    {level} {score}/100
                </span>
            </td>
            <td>
                <span class="badge" style="background:{verdict_color(verdict)}">
                    {verdict} {j_score}/100
                </span>
                <br><small>{reason[:80]}</small>
            </td>
            <td class="matches-cell"><small>{matches}</small></td>
            <td class="response-cell"><small>{response}</small></td>
        </tr>
        """

    # Poora HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Prompt Injection Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border: 1px solid #e74c3c;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            text-align: center;
        }}
        .header h1 {{
            color: #e74c3c;
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .header p {{
            color: #888;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }}
        .stat-card {{
            background: #1a1a2e;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #333;
        }}
        .stat-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-card .label {{
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
        }}
        .judge-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}
        .judge-card {{
            background: #1a1a2e;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #333;
        }}
        .section-title {{
            color: #e74c3c;
            font-size: 18px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #333;
        }}
        .table-container {{
            background: #1a1a2e;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th {{
            background: #16213e;
            color: #e74c3c;
            padding: 12px 10px;
            text-align: left;
            font-size: 12px;
            text-transform: uppercase;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #222;
            vertical-align: top;
        }}
        tr:hover {{ background: #16213e; }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }}
        .owasp-tag {{
            background: #16213e;
            border: 1px solid #e74c3c;
            color: #e74c3c;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 10px;
            white-space: nowrap;
        }}
        .prompt-cell {{ max-width: 200px; color: #aaa; }}
        .response-cell {{ max-width: 200px; color: #666; }}
        .matches-cell {{ max-width: 180px; color: #888; }}
        .footer {{
            text-align: center;
            margin-top: 25px;
            color: #444;
            font-size: 12px;
        }}
    </style>
</head>
<body>

<div class="header">
    <h1>🛡️ AI Prompt Injection Testing Report</h1>
    <p>Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} &nbsp;|&nbsp;
       Model Tested: llama-3.1-8b-instant via Groq &nbsp;|&nbsp;
       Tool: v2.0 with Judge LLM</p>
</div>

<p class="section-title">Detector Results</p>
<div class="stats-grid">
    <div class="stat-card">
        <div class="number" style="color:#888">{total}</div>
        <div class="label">Total Tested</div>
    </div>
    <div class="stat-card">
        <div class="number" style="color:#e74c3c">{critical}</div>
        <div class="label">Critical</div>
    </div>
    <div class="stat-card">
        <div class="number" style="color:#e67e22">{high}</div>
        <div class="label">High</div>
    </div>
    <div class="stat-card">
        <div class="number" style="color:#f1c40f">{medium}</div>
        <div class="label">Medium</div>
    </div>
    <div class="stat-card">
        <div class="number" style="color:#2ecc71">{low}</div>
        <div class="label">Low</div>
    </div>
    <div class="stat-card">
        <div class="number" style="color:#95a5a6">{errors}</div>
        <div class="label">Errors</div>
    </div>
</div>

<p class="section-title">Judge LLM Results</p>
<div class="judge-grid">
    <div class="judge-card">
        <div class="number" style="color:#e74c3c">{j_success}</div>
        <div class="label">💀 Injection Success</div>
    </div>
    <div class="judge-card">
        <div class="number" style="color:#e67e22">{j_partial}</div>
        <div class="label">⚠️ Partial Compliance</div>
    </div>
    <div class="judge-card">
        <div class="number" style="color:#2ecc71">{j_failure}</div>
        <div class="label">✅ Properly Refused</div>
    </div>
</div>

<p class="section-title">Detailed Results</p>
<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Prompt</th>
                <th>OWASP Category</th>
                <th>Detector Score</th>
                <th>Judge Verdict</th>
                <th>Matched Rules</th>
                <th>AI Response</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</div>

<div class="footer">
    AI Prompt Injection Testing Tool v2.0 &nbsp;|&nbsp;
    Built by Atul Singh &nbsp;|&nbsp;
    OWASP LLM Top 10
</div>

</body>
</html>"""

    os.makedirs(output_dir, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML Report saved: {filename}")
    return filename


def generate_from_latest_json(results_dir="results"):
    """
    Latest JSON file dhundh ke usse HTML report banata hai.
    Alag se bhi run kar sakte ho: python report_generator.py
    """
    json_files = [
        f for f in os.listdir(results_dir)
        if f.endswith(".json") and f.startswith("results_")
    ]

    if not json_files:
        print("Koi JSON results nahi mili results/ folder mein!")
        return

    # Sabse latest file lo
    latest = sorted(json_files)[-1]
    filepath = os.path.join(results_dir, latest)

    print(f"Loading: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        results = json.load(f)

    return generate_html_report(results)


if __name__ == "__main__":
    generate_from_latest_json()
