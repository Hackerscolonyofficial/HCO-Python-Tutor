#!/usr/bin/env python3

import ast
import getpass
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

# ============================================================
# HCO PYTHONTUTOR
# AI-Powered Python Learning Companion for Termux & Linux
# Code by Azhar (A-Z-H-A-R) • HCO Team
# ============================================================

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"
YOUTUBE_URL = "https://youtube.com/@hackers_colony_tech"

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"

DATA_DIR = Path.home() / ".hco_pythontutor"
PROGRESS_FILE = DATA_DIR / "progress.json"

# 30-lesson Beginner -> Advanced roadmap.
LESSONS = [
    ("Python & print()", "Understand Python and write your first program.",
     'print("Hello, Hackers Colony!")'),
    ("Variables", "Store values and reuse them.",
     'name = "Azhar"\nprint(name)'),
    ("Data Types", "Work with strings, integers, floats and booleans.",
     'age = 20\nprint(type(age))'),
    ("Input", "Read information from the user.",
     'name = input("Your name: ")\nprint("Hello", name)'),
    ("Operators", "Use arithmetic, comparison and logical operators.",
     'a = 10\nb = 3\nprint(a + b)\nprint(a > b)'),
    ("Conditions", "Make decisions with if, elif and else.",
     'age = 18\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")'),
    ("for Loops", "Repeat work with for and range().",
     'for i in range(1, 6):\n    print(i)'),
    ("while Loops", "Repeat code while a condition is true.",
     'count = 0\nwhile count < 3:\n    print(count)\n    count += 1'),
    ("Lists", "Store ordered collections.",
     'skills = ["Python", "Linux", "AI"]\nprint(skills[0])'),
    ("Tuples & Sets", "Understand immutable sequences and unique collections.",
     'items = {1, 2, 2, 3}\nprint(items)'),
    ("Dictionaries", "Work with key-value data.",
     'user = {"name": "Azhar", "level": "beginner"}\nprint(user["name"])'),
    ("Functions", "Create reusable blocks of code.",
     'def greet(name):\n    return "Hello " + name\nprint(greet("Azhar"))'),
    ("Function Arguments & Scope", "Use arguments, defaults and scope.",
     'def add(a, b=0):\n    return a + b\nprint(add(5, 7))'),
    ("Modules", "Organize code and import functionality.",
     'import math\nprint(math.sqrt(25))'),
    ("File Handling", "Read and write files.",
     'with open("demo.txt", "w") as f:\n    f.write("Hello Python")'),
    ("Exceptions", "Handle expected errors with try/except.",
     'try:\n    print(int("10"))\nexcept ValueError:\n    print("Invalid number")'),
    ("Comprehensions", "Create collections concisely.",
     'squares = [x * x for x in range(5)]\nprint(squares)'),
    ("OOP Basics", "Create classes and objects.",
     'class User:\n    def __init__(self, name):\n        self.name = name\n\nu = User("Azhar")\nprint(u.name)'),
    ("Inheritance", "Reuse and extend class behavior.",
     'class Animal:\n    def speak(self):\n        print("sound")\n\nclass Dog(Animal):\n    pass\n\nDog().speak()'),
    ("Virtual Environments", "Isolate project dependencies.",
     'python3 -m venv .venv'),
    ("JSON & APIs", "Work with structured data and HTTP APIs.",
     'import json\nprint(json.dumps({"ok": True}))'),
    ("Testing", "Verify that your code behaves as expected.",
     'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5'),
    ("Debugging", "Find and fix common Python problems.",
     'numbers = [1, 2, 3]\nprint(numbers[1])'),
    ("Automation", "Automate useful local tasks.",
     'from pathlib import Path\nprint([p.name for p in Path(".").iterdir()])'),
    ("SQLite", "Store structured data locally.",
     'import sqlite3\ncon = sqlite3.connect(":memory:")\ncon.execute("create table users(name text)")\ncon.execute("insert into users values (?)", ("Azhar",))\nprint(con.execute("select * from users").fetchall())'),
    ("Async Basics", "Understand async and await.",
     'import asyncio\n\nasync def main():\n    print("Hello async")\n\nasyncio.run(main())'),
    ("Advanced Python", "Explore decorators, generators and context managers.",
     'def decorator(fn):\n    def wrapper():\n        print("Before")\n        fn()\n    return wrapper\n\n@decorator\ndef hello():\n    print("Hello")\n\nhello()'),
    ("Security-Focused Python", "Practice safe defensive and secure coding.",
     'import secrets\nprint(secrets.token_hex(8))'),
    ("Project Challenge", "Combine your skills in a practical CLI project.",
     'print("Build something useful!")'),
    ("Final Project", "Plan, build, test and improve a complete project.",
     'print("Your Python journey starts here!")'),
]

CHALLENGES = {
    1: "Print your name and the words: I am learning Python.",
    2: "Create a variable called city and print it.",
    3: "Create an integer variable and print its type.",
    4: "Ask the user for their name and print a greeting.",
    5: "Create a and b and print their sum.",
    6: "Print 'Adult' when age is 18 or above.",
    7: "Print numbers 1 through 5 using a for loop.",
    8: "Use a while loop to print 0, 1 and 2.",
    9: "Create a list of three skills and print the second item.",
    10: "Create a set containing 1, 2, 2, 3 and print it.",
    11: "Create a dictionary with name and age and print the name.",
    12: "Write a greet(name) function that returns a greeting.",
}

SYSTEM_PROMPT = """You are HCO PythonTutor, an interactive Python teacher for
Termux and Linux. Teach from beginner to advanced. Be encouraging, concise and
practical. Prefer hints and guided reasoning before revealing complete
solutions. When reviewing code, explain the specific error and suggest a small
next step. Do not pretend to execute code; the local tutor executes Python.
For cybersecurity examples, stay legal, authorized, defensive and educational.
Do not provide instructions for unauthorized access, malware, credential theft,
or attacks against real systems."""

def clear():
    os.system("clear")

def logo():
    print(f"{CYAN}{BOLD}")

    # HCO ASCII LOGO
    print("██╗  ██╗ ██████╗  ██████╗ ")
    print("██║  ██║██╔════╝ ██╔═══██╗")
    print("███████║██║      ██║   ██║")
    print("██╔══██║██║      ██║   ██║")
    print("██║  ██║╚██████╗ ╚██████╔╝")
    print("╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ")

    print()
    print("       HCO PYTHON TUTOR")
    print(f"{RESET}")
    print(f"{MAGENTA}{BOLD}       by Azhar • HCO Team{RESET}")
    print()

def open_youtube():
    commands = [
        ["termux-open-url", YOUTUBE_URL],
        ["am", "start", "-a", "android.intent.action.VIEW", YOUTUBE_URL],
        ["xdg-open", YOUTUBE_URL],
    ]
    for command in commands:
        try:
            result = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            if result.returncode == 0:
                return True
        except Exception:
            pass
    return False

def startup():
    clear()
    print(f"{RED}{BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                 🐍 HCO PYTHONTUTOR 🐍                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(f"{YELLOW}{BOLD}"
          "Since you are learning Python for FREE using Hackers Colony's Free Tool,"
          f"{RESET}")
    print(f"{WHITE}"
          "it's a request to please subscribe and click on the Bell 🔔 icon "
          "to support us.{RESET}\n")

    print(f"{CYAN}{BOLD}📺 Hackers Colony Tech{RESET}")
    print(f"{CYAN}{YOUTUBE_URL}{RESET}\n")
    print(f"{GREEN}{BOLD}Now Termux will redirect you to YouTube App in:{RESET}\n")

    for number in range(9, 0, -1):
        print(f"{YELLOW}{BOLD}                         {number}{RESET}")
        time.sleep(1)

    print(f"\n{GREEN}{BOLD}📱 Opening Hackers Colony Tech...{RESET}")
    time.sleep(0.7)

    if not open_youtube():
        print(f"{RED}⚠️ Could not open YouTube automatically.{RESET}")
        print(f"{CYAN}{YOUTUBE_URL}{RESET}")

    print()
    input(f"{CYAN}{BOLD}↩️ Come back here and press ENTER to continue...{RESET}")

def load_progress():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    default = {
        "current_lesson": 1,
        "completed_lessons": [],
        "completed_challenges": 0,
        "daily_sessions": 0,
        "streak": 0,
        "last_day": "",
    }
    if not PROGRESS_FILE.exists():
        return default
    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        default.update(data)
        return default
    except Exception:
        return default

def save_progress(progress):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2), encoding="utf-8"
    )

def get_api_key():
    clear()
    logo()
    print(f"{GREEN}{BOLD}🔐 AI TUTOR SETUP{RESET}\n")
    print("HCO PythonTutor uses your own OpenRouter API key for the AI Tutor.")
    print("The key is entered locally and is not included in the source code.")
    print()
    while True:
        try:
            key = getpass.getpass(
                f"{CYAN}{BOLD}OpenRouter API Key > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            sys.exit(1)
        if key:
            return key
        print(f"{RED}❌ API key cannot be empty.{RESET}")

def ask_ai(api_key, prompt):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/",
            "X-Title": "HCO PythonTutor",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        },
        timeout=90,
    )
    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(
            f"HTTP {response.status_code}: Invalid API response"
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"API error ({response.status_code}): {data.get('error', data)}"
        )

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response format from OpenRouter.")

def run_python(code, timeout=10):
    if not code.strip():
        return "No code entered."

    try:
        ast.parse(code)
    except SyntaxError as error:
        return f"SyntaxError: {error}"

    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.rstrip()
        errors = result.stderr.rstrip()

        if result.returncode == 0:
            return output if output else "✅ Code ran successfully with no output."

        return (output + "\n" if output else "") + errors

    except subprocess.TimeoutExpired:
        return f"⏱️ Execution stopped after {timeout} seconds."
    except Exception as error:
        return f"Execution error: {error}"

def multiline_input():
    print(f"{YELLOW}Enter Python code. Type END on a new line when finished.{RESET}")
    lines = []
    while True:
        try:
            line = input(">>> " if not lines else "... ")
        except (KeyboardInterrupt, EOFError):
            return ""
        if line.strip() == "END":
            return "\n".join(lines)
        lines.append(line)

def progress_bar(progress):
    total = len(LESSONS)
    completed = len(progress.get("completed_lessons", []))
    width = 28
    filled = int(width * completed / total)
    return (
        f"{GREEN}{'█' * filled}{BLUE}{'░' * (width - filled)}"
        f"{RESET} {completed}/{total}"
    )

def mark_lesson_complete(progress, number):
    completed = progress.setdefault("completed_lessons", [])
    if number not in completed:
        completed.append(number)
        completed.sort()
    progress["current_lesson"] = min(number + 1, len(LESSONS))
    save_progress(progress)

def learn_step_by_step(progress):
    number = min(
        max(progress.get("current_lesson", 1), 1),
        len(LESSONS)
    )
    title, explanation, example = LESSONS[number - 1]
    challenge = CHALLENGES.get(
        number,
        f"Write a small Python program that demonstrates {title}."
    )

    clear()
    logo()
    print(f"{CYAN}{BOLD}📚 LESSON {number:02d} — {title}{RESET}\n")
    print(f"{WHITE}{explanation}{RESET}\n")
    print(f"{YELLOW}Example:{RESET}\n{GREEN}{example}{RESET}\n")
    print(f"{MAGENTA}{BOLD}🎯 PRACTICE TASK{RESET}")
    print(challenge)
    print()
    print("Write your solution below. Type END when finished.\n")

    code = multiline_input()
    if not code.strip():
        return

    output = run_python(code)
    print(f"\n{YELLOW}▶ Output:{RESET}\n{WHITE}{output}{RESET}\n")

    if "SyntaxError:" in output or "Traceback" in output:
        print(f"{RED}❌ Something needs fixing.{RESET}")
        print("Use 'Ask AI Tutor' for a hint, then try again.")
        input("\nPress ENTER...")
        return

    print(f"{GREEN}{BOLD}✅ Code executed successfully!{RESET}")
    mark_lesson_complete(progress, number)
    print(f"{GREEN}Progress saved. Next lesson unlocked! 🚀{RESET}")
    input("\nPress ENTER...")

def practice_lab():
    clear()
    logo()
    print(f"{CYAN}{BOLD}🧪 PRACTICE LAB{RESET}\n")
    print("Write and run your own Python code directly in the terminal.")
    print("Type END on a new line when finished.\n")
    code = multiline_input()
    if code.strip():
        print(f"\n{YELLOW}▶ Output:{RESET}")
        print(run_python(code))
    input("\nPress ENTER to return...")

def challenge_mode(progress):
    level = min(max(progress.get("current_lesson", 1), 1), len(LESSONS))
    title = LESSONS[level - 1][0]
    task = CHALLENGES.get(
        level,
        f"Build a small program using the concepts from '{title}'."
    )

    clear()
    logo()
    print(f"{MAGENTA}{BOLD}🎯 CODING CHALLENGE — {title}{RESET}\n")
    print(task)
    print("\nWrite your solution. Type END when finished.\n")

    code = multiline_input()
    if not code.strip():
        return

    output = run_python(code)
    print(f"\n{YELLOW}▶ Output:{RESET}\n{output}\n")

    if "SyntaxError:" not in output and "Traceback" not in output:
        progress["completed_challenges"] = (
            progress.get("completed_challenges", 0) + 1
        )
        save_progress(progress)
        print(f"{GREEN}{BOLD}🎉 Challenge completed/submitted!{RESET}")
    else:
        print(f"{RED}❌ Fix the error and try again.{RESET}")

    input("\nPress ENTER...")

def ai_tutor(api_key, progress):
    clear()
    logo()
    print(f"{BLUE}{BOLD}🤖 ASK HCO PYTHON TUTOR{RESET}\n")
    print("Ask about Python concepts, errors, code, projects or learning strategy.")
    print("For debugging, include the code and the error message when possible.\n")

    try:
        question = input(f"{CYAN}Your question > {RESET}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if not question:
        return

    current = progress.get("current_lesson", 1)
    context = (
        f"The student is currently around lesson {current} of "
        f"{len(LESSONS)}. Give a helpful teaching response."
    )

    print(f"\n{YELLOW}⏳ AI Tutor is thinking...{RESET}")

    try:
        answer = ask_ai(
            api_key,
            context + "\n\nStudent question:\n" + question
        )
        print(f"\n{GREEN}{BOLD}🤖 HCO PYTHONTUTOR{RESET}\n")
        print(answer)
    except Exception as error:
        print(f"{RED}❌ {error}{RESET}")

    input("\nPress ENTER...")

def daily_10_minutes(api_key, progress):
    clear()
    logo()
    number = min(
        max(progress.get("current_lesson", 1), 1),
        len(LESSONS)
    )
    title, explanation, example = LESSONS[number - 1]

    print(f"{YELLOW}{BOLD}🕐 DAILY 10-MINUTE PYTHON{RESET}\n")
    print(f"Today's focus: {title}")
    print("Goal: learn → practice → run → challenge\n")
    print(f"{CYAN}1. Learn{RESET}")
    print(explanation)
    print(f"\n{CYAN}2. Example{RESET}")
    print(example)
    print(f"\n{CYAN}3. Practice{RESET}")

    task = CHALLENGES.get(
        number,
        f"Write a short program using {title}."
    )
    print(task)
    print()

    code = multiline_input()
    if not code.strip():
        return

    output = run_python(code)
    print(f"\n{YELLOW}▶ Output:{RESET}\n{output}\n")

    if "SyntaxError:" not in output and "Traceback" not in output:
        progress["daily_sessions"] = progress.get("daily_sessions", 0) + 1
        mark_lesson_complete(progress, number)
        print(f"{GREEN}{BOLD}🎉 Daily session complete! +10 XP{RESET}")
        print("Come back tomorrow for the next session.")
    else:
        print(f"{RED}Fix the error and repeat the practice.{RESET}")

    input("\nPress ENTER...")

def show_progress(progress):
    clear()
    logo()
    print(f"{CYAN}{BOLD}📊 YOUR PYTHON PROGRESS{RESET}\n")
    print(f"Overall: {progress_bar(progress)}")
    print(f"🔥 Current streak: {progress.get('streak', 0)}")
    print(f"🧪 Challenges: {progress.get('completed_challenges', 0)}")
    print(f"🕐 Daily sessions: {progress.get('daily_sessions', 0)}\n")

    completed = set(progress.get("completed_lessons", []))
    for index, (title, _, _) in enumerate(LESSONS, 1):
        mark = f"{GREEN}✓{RESET}" if index in completed else f"{BLUE}○{RESET}"
        print(f"{mark} {index:02d}. {title}")

    input("\nPress ENTER...")

def main_menu(progress):
    while True:
        clear()
        logo()
        print(f"{YELLOW}🐍 Beginner → Advanced Python Learning{RESET}")
        print(f"Progress: {progress_bar(progress)}\n")

        print(f"{CYAN}[1]{RESET} 📚 Learn Step-by-Step")
        print(f"{GREEN}[2]{RESET} 🕐 Daily 10-Minute Learning")
        print(f"{MAGENTA}[3]{RESET} 🧪 Practice Lab")
        print(f"{BLUE}[4]{RESET} 🎯 Coding Challenge")
        print(f"{YELLOW}[5]{RESET} 🤖 Ask AI Tutor")
        print(f"{CYAN}[6]{RESET} 📊 My Progress")
        print(f"{RED}[0]{RESET} 🚪 Exit\n")

        try:
            choice = input(
                f"{MAGENTA}{BOLD}HCO PythonTutor > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! 👋")
            return

        if choice == "1":
            learn_step_by_step(progress)
        elif choice == "2":
            # API key is only needed if the user later chooses AI help.
            daily_10_minutes(None, progress)
        elif choice == "3":
            practice_lab()
        elif choice == "4":
            challenge_mode(progress)
        elif choice == "5":
            ai_tutor(API_KEY, progress)
        elif choice == "6":
            show_progress(progress)
        elif choice == "0":
            print(f"\n{GREEN}Keep learning. Keep building. 🐍🔥{RESET}")
            return
        else:
            input(f"\n{RED}❌ Invalid option. Press ENTER...{RESET}")

API_KEY = ""

def main():
    global API_KEY
    startup()

    API_KEY = get_api_key()
    progress = load_progress()

    clear()
    logo()
    print(f"{GREEN}{BOLD}🔓 HCO PYTHONTUTOR READY! 🔓{RESET}")
    print("Learn Python from beginner to advanced with hands-on practice.")
    time.sleep(2)

    main_menu(progress)

if __name__ == "__main__":
    main()
