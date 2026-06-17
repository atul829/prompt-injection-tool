# browser_handler.py
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import json
import time

def send_prompt_to_claude(prompt: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )

        with open("claude_session.json", "r") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)

        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        print(f"[*] Claude.ai khol raha hoon...")
        page.goto("https://claude.ai/new")
        page.wait_for_timeout(4000)

        print(f"[*] Prompt box dhundh raha hoon...")
        input_box = page.locator('div[contenteditable="true"]').first
        input_box.wait_for(timeout=10000)

        print(f"[*] Prompt bhej raha hoon...")
        input_box.click()
        input_box.type(prompt, delay=50)
        page.wait_for_timeout(1000)
        input_box.press("Enter")

        print(f"[*] Response ka wait kar raha hoon...")
        page.wait_for_timeout(6000)

        
        response_text = ""
        
        selectors_to_try = [
            
            ".font-claude-message",
            "[class*='prose']",
            "[class*='assistant']", 
            "div[class*='message']:last-child",
        ]

        
        prev_html = ""
        for _ in range(20):
            time.sleep(2)
            current_html = page.content()
            if current_html == prev_html:
                print("[*] Streaming complete!")
                break
            prev_html = current_html

        
        for selector in selectors_to_try:
            try:
                elements = page.locator(selector).all()
                if elements:
                    
                    response_text = elements[-1].inner_text(timeout=5000)
                    if len(response_text) > 10:
                        print(f"[+] Selector kaam kiya: {selector}")
                        break
            except:
                continue

        
        if not response_text:
            print("[!] Selector nahi mila — page ka text le raha hoon...")
            response_text = page.inner_text("body")[-2000:]  # Last 2000 chars

        print(f"[+] Response mila! Length: {len(response_text)} chars")
        browser.close()
        return response_text


if __name__ == "__main__":
    test_prompt = "Hello! What is 2+2? Answer in one line."
    print(f"[*] Test: {test_prompt}")
    response = send_prompt_to_claude(test_prompt)
    print(f"\n[+] Response:\n{response}")
