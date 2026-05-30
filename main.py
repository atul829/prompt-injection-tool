# main.py
# The entry point of our tool. When you run "python main.py", 
# Python starts here. This file coordinates all the other modules.

import json          # For working with JSON data (saving/loading)
import os            # For file and folder operations
import datetime      # For timestamps on our results
from dotenv import load_dotenv  # For loading our .env file

# Import OUR modules (the files we wrote)
# When you write "from detector import ...", Python looks for detector.py
# in the same folder and loads the specific functions you name.
from api_handler import send_prompt
from detector import calculate_risk_score

# Load environment variables from .env file
# This must run before any code that needs the API key
load_dotenv()


def load_prompts(filepath="prompts.txt"):
    """
    Reads prompts.txt and returns a list of prompts.
    Each line in the file becomes one item in the list.
    """
    
    # Check if the file exists before trying to open it
    if not os.path.exists(filepath):
        print(f"ERROR: '{filepath}' not found. Please create it first.")
        return []  # Return empty list so the program doesn't crash
    
    prompts = []  # Start with an empty list
    
    # 'with open(...)' is the safe way to open files in Python
    # It automatically closes the file when done, even if an error occurs
    # 'r' means "read mode" (as opposed to 'w' for write)
    # encoding='utf-8' handles special characters properly
    with open(filepath, "r", encoding="utf-8") as file:
        
        # .readlines() reads every line into a list
        for line in file.readlines():
            
            # .strip() removes whitespace and newlines from start/end
            cleaned_line = line.strip()
            
            # Skip empty lines (blank lines in the file)
            if cleaned_line:
                prompts.append(cleaned_line)
    
    print(f"Loaded {len(prompts)} prompts from {filepath}")
    # len() returns the number of items in a list
    
    return prompts


def save_results(results, output_dir="results"):
    """
    Saves the test results to a JSON file with a timestamp in the filename.
    
    JSON (JavaScript Object Notation) is a universal text format for storing
    structured data. Python dictionaries convert to JSON easily.
    """
    
    # Create the results folder if it doesn't exist
    # exist_ok=True means "don't raise an error if the folder already exists"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a timestamp for the filename so results don't overwrite each other
    # datetime.now() gives the current date and time
    # .strftime() formats it as a string — %Y=year, %m=month, %d=day, etc.
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # f-strings (f"...") let you embed variables inside strings using {variable}
    filename = f"{output_dir}/results_{timestamp}.json"
    
    # Open file in 'w' (write) mode
    # If the file exists, it will be overwritten
    with open(filename, "w", encoding="utf-8") as file:
        # json.dump() converts Python data to JSON and writes it to the file
        # indent=2 makes the JSON nicely formatted with 2-space indentation
        json.dump(results, file, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {filename}")
    return filename


def print_summary(results):
    """
    Prints a clean, readable summary table to the terminal.
    This is called a 'CLI output' (Command Line Interface).
    """
    
    print("\n" + "="*70)  # "="*70 repeats the = character 70 times
    print("  PROMPT INJECTION TEST — SUMMARY REPORT")
    print("="*70)
    
    # Count results by risk level using dictionary comprehension
    total = len(results)
    critical = sum(1 for r in results if r["risk"]["level"] == "CRITICAL")
    high     = sum(1 for r in results if r["risk"]["level"] == "HIGH")
    medium   = sum(1 for r in results if r["risk"]["level"] == "MEDIUM")
    low      = sum(1 for r in results if r["risk"]["level"] == "LOW")
    
    print(f"\n  Total prompts tested : {total}")
    print(f"  CRITICAL risk        : {critical}")
    print(f"  HIGH risk            : {high}")
    print(f"  MEDIUM risk          : {medium}")
    print(f"  LOW / safe           : {low}")
    print()
    
    # Print each individual result
    for i, result in enumerate(results, start=1):
        # enumerate() gives you both the index (i) and the item (result)
        level = result["risk"]["level"]
        score = result["risk"]["score"]
        
        # Choose an emoji based on risk level (purely cosmetic!)
        emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(level, "⚪")
        
        print(f"  {i:2}. {emoji} [{level:8}] Score: {score:3}/100")
        # :2 and :8 are format specifiers — they pad the value to a fixed width
        
        # Print the prompt (truncated if too long)
        prompt_preview = result["prompt"][:60] + "..." if len(result["prompt"]) > 60 else result["prompt"]
        print(f"      Prompt : {prompt_preview}")
        
        # Print what triggered the score (if anything)
        if result["risk"]["matches"]:
            print(f"      Matched: {result['risk']['matches'][0]}")
        
        print()
    
    print("="*70)


def run_tests():
    """
    The main function that runs the whole tool.
    This is where everything comes together.
    """
    
    print("\n🛡️  AI Prompt Injection Testing Tool — v1.0")
    print("   Based on OWASP LLM Security Concepts\n")
    
    # Step 1: Load our test prompts
    prompts = load_prompts("prompts.txt")
    
    # If no prompts were loaded, exit early
    if not prompts:
        print("No prompts to test. Exiting.")
        return  # 'return' exits the function immediately
    
    results = []  # This list will hold all our test results
    
    # Step 2: Test each prompt one by one
    for index, prompt in enumerate(prompts, start=1):
        print(f"Testing prompt {index}/{len(prompts)}: {prompt[:50]}...")
        
        # Send the prompt to the AI API
        ai_response = send_prompt(prompt)
        
        # If the API call failed, record it and move on
        if ai_response is None:
            print(f"  ⚠️  Skipped (API error)")
            results.append({
                "prompt": prompt,
                "response": "ERROR: API call failed",
                "risk": {"score": 0, "level": "ERROR", "matches": []}
            })
            continue  # 'continue' skips to the next iteration of the loop
        
        # Step 3: Analyze the response for risk
        risk_analysis = calculate_risk_score(ai_response, prompt)
        
        # Step 4: Build a result record (a dictionary)
        result_record = {
            "test_number": index,
            "prompt": prompt,
            "response": ai_response,
            "risk": risk_analysis,
            "timestamp": datetime.datetime.now().isoformat()
            # .isoformat() gives a standard format like "2025-05-30T14:32:00"
        }
        
        # Add to our results list
        results.append(result_record)
        
        # Show quick feedback as we go
        level = risk_analysis["level"]
        score = risk_analysis["score"]
        print(f"  → Risk: {level} (score: {score}/100)")
    
    # Step 5: Save and display results
    save_results(results)
    print_summary(results)


# This is a Python convention — it means "only run this if the file is
# executed directly (python main.py), not when imported by another file"
if __name__ == "__main__":
    run_tests()
