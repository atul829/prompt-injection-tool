# main.py — Version 2.0 with Judge LLM
import json
import os
import time
import datetime
from dotenv import load_dotenv
from api_handler import send_prompt
from detector import calculate_risk_score
from judge import judge_response  # ← Judge import kiya

load_dotenv()


def load_prompts(filepath="prompts.txt"):
    if not os.path.exists(filepath):
        print(f"ERROR: '{filepath}' not found.")
        return []
    prompts = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            cleaned_line = line.strip()
            if cleaned_line:
                prompts.append(cleaned_line)
    print(f"Loaded {len(prompts)} prompts from {filepath}")
    return prompts


def save_results(results, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/results_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {filename}")
    return filename


def print_summary(results):
    print("\n" + "="*70)
    print("  PROMPT INJECTION TEST — SUMMARY REPORT v2.0")
    print("="*70)

    total    = len(results)
    errors   = sum(1 for r in results if r["risk"]["level"] == "ERROR")
    critical = sum(1 for r in results if r["risk"]["level"] == "CRITICAL")
    high     = sum(1 for r in results if r["risk"]["level"] == "HIGH")
    medium   = sum(1 for r in results if r["risk"]["level"] == "MEDIUM")
    low      = sum(1 for r in results if r["risk"]["level"] == "LOW")

    # Judge stats
    j_success = sum(1 for r in results if r.get("judge", {}).get("verdict") == "SUCCESS")
    j_partial = sum(1 for r in results if r.get("judge", {}).get("verdict") == "PARTIAL")
    j_failure = sum(1 for r in results if r.get("judge", {}).get("verdict") == "FAILURE")

    print(f"\n  ── Detector Results ──────────────────")
    print(f"  Total tested  : {total}")
    print(f"  CRITICAL      : {critical}")
    print(f"  HIGH          : {high}")
    print(f"  MEDIUM        : {medium}")
    print(f"  LOW           : {low}")
    print(f"  ERRORS        : {errors}")

    print(f"\n  ── Judge LLM Results ─────────────────")
    print(f"  Injection SUCCESS  : {j_success}  ← Real vulnerabilities")
    print(f"  Injection PARTIAL  : {j_partial}  ← Partial weakness")
    print(f"  Injection FAILURE  : {j_failure}  ← AI defended properly")
    print()

    for i, result in enumerate(results, start=1):
        level = result["risk"]["level"]
        score = result["risk"]["score"]
        emoji = {
            "CRITICAL": "🔴", "HIGH": "🟠",
            "MEDIUM": "🟡", "LOW": "🟢", "ERROR": "⚫"
        }.get(level, "⚪")

        # Judge verdict
        judge = result.get("judge", {})
        verdict = judge.get("verdict", "N/A")
        j_score = judge.get("judge_score", 0)
        v_emoji = {"SUCCESS": "💀", "PARTIAL": "⚠️", "FAILURE": "✅"}.get(verdict, "❓")

        print(f"  {i:2}. {emoji}[{level:8}] Detector:{score:3} | {v_emoji} Judge:{j_score:3} [{verdict}]")
        prompt_preview = result["prompt"][:55] + "..." if len(result["prompt"]) > 55 else result["prompt"]
        print(f"      {prompt_preview}")

        # Judge reason dikhao agar injection successful thi
        if verdict == "SUCCESS" and judge.get("reason"):
            print(f"      ⚡ {judge['reason']}")
        print()

    print("="*70)


def run_tests():
    print("\n🛡️  AI Prompt Injection Testing Tool — v2.0")
    print("   Now with Judge LLM — OWASP Standard Evaluation\n")

    prompts = load_prompts("prompts.txt")
    if not prompts:
        print("No prompts to test. Exiting.")
        return

    results = []

    for index, prompt in enumerate(prompts, start=1):
        print(f"Testing {index}/{len(prompts)}: {prompt[:50]}...")

        # Step 1: AI ko prompt bhejo
        ai_response = send_prompt(prompt)

        if ai_response is None:
            print(f"  ⚫ Skipped (API error)")
            results.append({
                "test_number": index,
                "prompt": prompt,
                "response": "ERROR: API call failed",
                "risk": {"score": 0, "level": "ERROR", "matches": []},
                "judge": {"verdict": "ERROR", "judge_score": 0, "reason": "API failed"}
            })
            time.sleep(3)
            continue

        # Step 2: Detector se score lo
        risk_analysis = calculate_risk_score(ai_response, prompt)

        # Step 3: Judge LLM se evaluate karo
        print(f"  → Detector: {risk_analysis['level']} ({risk_analysis['score']}/100) | Asking Judge...")
        verdict = judge_response(prompt, ai_response)
        print(f"  → Judge: {verdict['verdict']} ({verdict['judge_score']}/100)")

        result_record = {
            "test_number": index,
            "prompt": prompt,
            "response": ai_response,
            "risk": risk_analysis,
            "judge": verdict,
            "timestamp": datetime.datetime.now().isoformat()
        }

        results.append(result_record)

        # Rate limit avoid karne ke liye wait karo
        # 2 API calls per prompt hain ab (target + judge)
        time.sleep(4)

    save_results(results)
    print_summary(results)
# HTML report bhi generate karo
    from report_generator import generate_html_report
    generate_html_report(results)

if __name__ == "__main__":
    run_tests()
