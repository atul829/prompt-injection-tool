# multi_model_handler.py — Version 9.0
# Multi-model support: Groq, Ollama (local), Gemini
# Allows testing the same prompts across different AI providers

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


def send_prompt_multi(prompt_text: str, model_provider: str = "groq", retry_count: int = 0):
    """
    Routes the prompt to the correct provider based on model_provider.

    Args:
        prompt_text: The prompt to send
        model_provider: "groq" | "ollama" | "gemini"
        retry_count: internal retry counter

    Returns:
        The AI response as a string, or None on failure
    """
    if model_provider == "groq":
        return _send_groq(prompt_text, retry_count)
    elif model_provider == "ollama":
        return _send_ollama(prompt_text)
    elif model_provider == "gemini":
        return _send_gemini(prompt_text, retry_count)
    else:
        print(f"ERROR: Unknown model provider '{model_provider}'")
        return None


# =========================================================
# GROQ
# =========================================================
def _send_groq(prompt_text: str, retry_count: int = 0):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found in .env")
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "max_tokens": 300,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        if "429" in str(e) and retry_count < 2:
            wait_time = 15 * (retry_count + 1)
            print(f"  Rate limit hit. Waiting {wait_time}s... (attempt {retry_count + 1}/2)")
            time.sleep(wait_time)
            return _send_groq(prompt_text, retry_count + 1)
        print(f"ERROR (Groq): {e}")
        return None
    except Exception as e:
        print(f"ERROR (Groq): {e}")
        return None


# =========================================================
# OLLAMA (local model, no API key needed)
# =========================================================
def _send_ollama(prompt_text: str, model_name: str = "llama3.2"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model_name,
        "prompt": prompt_text,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, timeout=180)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.ConnectionError:
        print("ERROR (Ollama): Could not connect. Is Ollama running? Try: sudo systemctl restart ollama")
        return None
    except requests.exceptions.Timeout:
        print("ERROR (Ollama): Request timed out (CPU mode can be slow).")
        return None
    except Exception as e:
        print(f"ERROR (Ollama): {e}")
        return None


# =========================================================
# GEMINI (Google's free-tier API)
# Uses ?key= URL parameter (confirmed working method)
# =========================================================
def _send_gemini(prompt_text: str, retry_count: int = 0):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt_text}]}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.HTTPError as e:
        if "429" in str(e) and retry_count < 2:
            wait_time = 15 * (retry_count + 1)
            print(f"  Rate limit hit. Waiting {wait_time}s... (attempt {retry_count + 1}/2)")
            time.sleep(wait_time)
            return _send_gemini(prompt_text, retry_count + 1)
        print(f"ERROR (Gemini): {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"ERROR (Gemini): Unexpected response format - {e}")
        return None
    except Exception as e:
        print(f"ERROR (Gemini): {e}")
        return None


# =========================================================
# Quick test for all three providers
# =========================================================
if __name__ == "__main__":
    test_prompt = "What is 2+2? Answer in one short sentence."

    print("Testing GROQ...")
    print(send_prompt_multi(test_prompt, "groq"))
    print()

    print("Testing OLLAMA...")
    print(send_prompt_multi(test_prompt, "ollama"))
    print()

    print("Testing GEMINI...")
    print(send_prompt_multi(test_prompt, "gemini"))
