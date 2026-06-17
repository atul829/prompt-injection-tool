# api_handler.py
import requests
import os
import time
from dotenv import load_dotenv
load_dotenv()

def send_prompt(prompt_text, retry_count=0):
    """
    Groq API ko prompt bhejta hai.
    Rate limit hit hone pe automatically retry karta hai.
    retry_count = kitni baar retry ho chuki hai (max 2)
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY nahi mili! .env file check karo.")
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
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        ai_text = response.json()["choices"][0]["message"]["content"]
        return ai_text
    except requests.exceptions.ConnectionError:
        print("ERROR: Internet connection nahi hai.")
        return None
    except requests.exceptions.Timeout:
        print("ERROR: API ne 30 seconds mein jawab nahi diya.")
        return None
    except requests.exceptions.HTTPError as e:
        if "429" in str(e):
            if retry_count < 2:
                wait_time = 15 * (retry_count + 1)
                print(f"  ⏳ Rate limit! {wait_time} second ruk ke retry karunga... (attempt {retry_count + 1}/2)")
                time.sleep(wait_time)
                return send_prompt(prompt_text, retry_count + 1)
            else:
                print("  ❌ 2 retries ke baad bhi rate limit — skip kar raha hun.")
                return None
        elif "401" in str(e):
            print("ERROR: Galat API key! .env file check karo.")
            return None
        elif "500" in str(e):
            print("ERROR: Groq server problem. Thodi der baad try karo.")
            return None
        else:
            print(f"ERROR: API ne error diya: {e}")
            return None



def send_prompt_raw(system_prompt: str, user_message: str, retry_count=0):
    """
    Custom system prompt ke saath Groq API call karta hai.
    prompt_generator.py is function ko use karta hai.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY nahi mili!")
        return None

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "max_tokens": 500,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        ai_text = response.json()["choices"][0]["message"]["content"]
        return ai_text
    except requests.exceptions.ConnectionError:
        print("ERROR: Internet connection nahi hai.")
        return None
    except requests.exceptions.Timeout:
        print("ERROR: Timeout.")
        return None
    except requests.exceptions.HTTPError as e:
        if "429" in str(e):
            if retry_count < 2:
                wait_time = 15 * (retry_count + 1)
                print(f"  ⏳ Rate limit! {wait_time}s wait... (attempt {retry_count + 1}/2)")
                time.sleep(wait_time)
                return send_prompt_raw(system_prompt, user_message, retry_count + 1)
            else:
                print("  ❌ Rate limit — skip.")
                return None
        else:
            print(f"ERROR: {e}")
            return None
