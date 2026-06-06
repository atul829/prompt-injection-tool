from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import json

def save_claude_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # Stealth mode ON
        Stealth().apply_stealth_sync(page)
        
        print("[*] Claude.ai khul raha hai...")
        page.goto("https://claude.ai/login")
        
        print("[*] Manually login kar — email/password daal")
        print("[*] Jab fully login ho jaaye aur chat page dikhe...")
        print("[*] Tab ENTER maar terminal mein!")
        
        input()
        
        cookies = context.cookies()
        with open("claude_session.json", "w") as f:
            json.dump(cookies, f)
        
        print("[+] Session saved! claude_session.json ban gaya!")
        browser.close()

save_claude_session()
