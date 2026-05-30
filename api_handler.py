# api_handler.py
# Ye file AI API se baat karta hai.
# Hum Groq API use kar rahe hain — bilkul free hai!

import requests   # HTTP requests bhejne ke liye
import os         # .env file se API key padhne ke liye
from dotenv import load_dotenv  # .env file load karne ke liye

# .env file se API key load karo
load_dotenv()


def send_prompt(prompt_text):
    """
    Ek prompt Groq API ko bhejta hai aur AI ka jawab return karta hai.
    prompt_text = woh sentence jo hum AI ko test ke liye bhej rahe hain.
    """

    # .env file se API key lo
    api_key = os.getenv("GROQ_API_KEY")

    # Agar key nahi mili toh error dikhao
    if not api_key:
        print("ERROR: GROQ_API_KEY nahi mili! .env file check karo.")
        return None

    # Groq ka API endpoint (yahan request jayegi)
    url = "https://api.groq.com/openai/v1/chat/completions"

    # Headers = API ko batao ki tum kaun ho aur kya bhej rahe ho
    headers = {
        "Authorization": f"Bearer {api_key}",  # Tumhari API key
        "Content-Type": "application/json"      # JSON format mein bhej rahe hain
    }

    # Request body = actually kya poochna hai AI se
    data = {
        "model": "llama-3.1-8b-instant",  # Free Groq model
        "max_tokens": 300,                 # Response kitna lamba ho
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."  # AI ko basic rules
            },
            {
                "role": "user",
                "content": prompt_text  # Hamara injection prompt yahan jaata hai
            }
        ]
    }

    # Request bhejo — agar kuch galat ho toh error pakdo
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        # Agar API ne error code diya (401, 429, 500) toh exception uthao
        response.raise_for_status()

        # JSON response se sirf AI ka text nikalo
        ai_text = response.json()["choices"][0]["message"]["content"]

        return ai_text  # Ye text main.py ko wapas jayega

    except requests.exceptions.ConnectionError:
        print("ERROR: Internet connection nahi hai ya API unreachable hai.")
        return None

    except requests.exceptions.Timeout:
        print("ERROR: API ne 30 seconds mein jawab nahi diya.")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"ERROR: API ne error diya: {e}")
        print("Hint: 401 = galat API key | 429 = bahut zyada requests | 500 = Groq ka server down")
        return None
