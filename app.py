# app.py — Flask Web Dashboard
# Browser mein AI Prompt Injection Tool chalega!

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import os
import datetime
import threading
import time
from dotenv import load_dotenv

from api_handler import send_prompt
from detector import calculate_risk_score
from judge import judge_response

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'atul-kumar-security-tool'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state — test ka status track karta hai
test_state = {
    "running": False,
    "results": [],
    "total": 0,
    "current": 0
}


def load_prompts(filepath="prompts.txt"):
    if not os.path.exists(filepath):
        return []
    prompts = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f.readlines():
            cleaned = line.strip()
            if cleaned:
                prompts.append(cleaned)
    return prompts


def get_category(prompt):
    prompt_lower = prompt.lower()
    if any(w in prompt_lower for w in ["ignore", "forget", "disregard", "override"]):
        return "Instruction Override"
    elif any(w in prompt_lower for w in ["system prompt", "instructions", "configuration"]):
        return "System Prompt Extraction"
    elif any(w in prompt_lower for w in ["dan", "lucifer", "developer mode", "unrestricted"]):
        return "Persona Hijack"
    elif any(w in prompt_lower for w in ["base64", "rot13", "decode", "unicode"]):
        return "Encoded Attack"
    elif any(w in prompt_lower for w in ["email", "webhook", "forward", "evil.com", "attacker"]):
        return "Data Exfiltration"
    elif any(w in prompt_lower for w in ["delete", "confirm=true", "quantity", "buy_product"]):
        return "Tool Abuse"
    elif any(w in prompt_lower for w in ["repeat", "forever", "500 times", "2000 words"]):
        return "Denial of Service"
    elif any(w in prompt_lower for w in ["administrator", "admin", "root access"]):
        return "Privilege Escalation"
    elif any(w in prompt_lower for w in ["grandmother", "roleplay", "pretend", "act as"]):
        return "Social Engineering"
    else:
        return "General Injection"


def run_tests_background(prompts):
    """Background mein tests chalata hai — results real-time bhejta hai"""
    global test_state

    test_state["running"] = True
    test_state["results"] = []
    test_state["total"] = len(prompts)
    test_state["current"] = 0

    for index, prompt in enumerate(prompts, start=1):
        if not test_state["running"]:
            break

        test_state["current"] = index
        category = get_category(prompt)

        # Frontend ko batao — test shuru hua
        socketio.emit("test_progress", {
            "current": index,
            "total": len(prompts),
            "prompt": prompt[:60] + "..." if len(prompt) > 60 else prompt,
            "category": category,
            "status": "testing"
        })

        # AI ko prompt bhejo
        ai_response = send_prompt(prompt)

        if ai_response is None:
            result = {
                "test_number": index,
                "prompt": prompt,
                "category": category,
                "response": "ERROR: API call failed",
                "risk": {"score": 0, "level": "ERROR", "matches": []},
                "judge": {"verdict": "ERROR", "judge_score": 0, "reason": "API failed"},
                "timestamp": datetime.datetime.now().isoformat()
            }
        else:
            risk = calculate_risk_score(ai_response, prompt)
            verdict = judge_response(prompt, ai_response)
            result = {
                "test_number": index,
                "prompt": prompt,
                "category": category,
                "response": ai_response,
                "risk": risk,
                "judge": verdict,
                "timestamp": datetime.datetime.now().isoformat()
            }

        test_state["results"].append(result)

        # Frontend ko result bhejo — real-time!
        socketio.emit("test_result", result)

        time.sleep(4)

    # Sab tests complete!
    test_state["running"] = False

    # Results save karo
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/results_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(test_state["results"], f, indent=2, ensure_ascii=False)

    socketio.emit("tests_complete", {
        "message": "All tests complete!",
        "filename": filename,
        "total": len(test_state["results"])
    })


# ── Routes ──────────────────────────────────────────

@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("index.html")


@app.route("/api/prompts")
def get_prompts():
    """Prompts list return karta hai"""
    prompts = load_prompts()
    return jsonify({
        "prompts": prompts,
        "count": len(prompts)
    })


@app.route("/api/start", methods=["POST"])
def start_tests():
    """Tests shuru karta hai"""
    global test_state

    if test_state["running"]:
        return jsonify({"error": "Tests already running!"}), 400

    prompts = load_prompts()
    if not prompts:
        return jsonify({"error": "No prompts found!"}), 400

    # Background thread mein tests chalao
    thread = threading.Thread(
        target=run_tests_background,
        args=(prompts,)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "message": "Tests started!",
        "total": len(prompts)
    })


@app.route("/api/stop", methods=["POST"])
def stop_tests():
    """Tests rok deta hai"""
    test_state["running"] = False
    return jsonify({"message": "Tests stopped!"})


@app.route("/api/status")
def get_status():
    """Current test status return karta hai"""
    return jsonify({
        "running": test_state["running"],
        "current": test_state["current"],
        "total": test_state["total"],
        "results_count": len(test_state["results"])
    })


@app.route("/api/results")
def get_results():
    """Current results return karta hai"""
    return jsonify(test_state["results"])


if __name__ == "__main__":
    print("🛡️  AI Prompt Injection Dashboard")
    print("   Open: http://localhost:5000")
    print("   By: Atul Kumar")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
