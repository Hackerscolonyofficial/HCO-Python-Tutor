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
# AI-Powered Interactive Python Learning Companion
# For Termux & Linux
#
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


# ============================================================
# 30-LESSON BEGINNER → ADVANCED PYTHON ROADMAP
# ============================================================

LESSONS = [

    {
        "title": "Python & print()",
        "goal": "Understand what Python is and write your first program.",
        "steps": [
            (
                "What is Python?",
                "Python is a programming language. You write instructions in Python and the Python interpreter executes them."
            ),
            (
                "What is print()?",
                "print() is a built-in Python function used to display information on the screen."
            ),
            (
                "What do the parentheses mean?",
                "The parentheses are used to pass information to a function. In print(\"Hello\"), the text inside the parentheses is given to print()."
            ),
            (
                "What are quotes?",
                "Text is called a string in Python. Strings are normally written inside quotes, such as \"Hello\"."
            ),
            (
                "What does >>> mean?",
                "When Python is waiting for interactive input, it may display >>>. This is a prompt from the interpreter. You do not type >>> yourself."
            ),
            (
                "What does ... mean?",
                "In HCO PythonTutor, ... means the tutor is waiting for another line of your code."
            ),
            (
                "What does END mean?",
                "HCO PythonTutor uses END to know that you have finished entering a multi-line program. Type END alone on a new line."
            ),
        ],
        "example": 'print("Hello, Hackers Colony!")',
        "task": "Print your name and then print: I am learning Python.",
        "hint": 'Use two print() statements, for example: print("Azhar")'
    },

    {
        "title": "Variables",
        "goal": "Learn how to store information using variables.",
        "steps": [
            (
                "What is a variable?",
                "A variable is a name that refers to a value. It lets your program store and reuse information."
            ),
            (
                "How do we create one?",
                "Use a variable name, followed by =, followed by a value."
            ),
            (
                "What does = mean?",
                "In Python, = assigns a value to a variable. It does not mean mathematical equality."
            ),
            (
                "How do we use a variable?",
                "Write the variable name wherever you want to use the stored value."
            ),
        ],
        "example": 'name = "Azhar"\nprint(name)',
        "task": "Create a variable called city and print it.",
        "hint": 'Try: city = "YourCity"'
    },

    {
        "title": "Data Types",
        "goal": "Understand strings, integers, floats and booleans.",
        "steps": [
            (
                "What is a data type?",
                "A data type describes what kind of value you are working with."
            ),
            (
                "String",
                'A string is text. Example: "Hello"'
            ),
            (
                "Integer",
                "An integer is a whole number. Example: 25"
            ),
            (
                "Float",
                "A float is a number that can contain a decimal point. Example: 3.14"
            ),
            (
                "Boolean",
                "A boolean has one of two values: True or False."
            ),
            (
                "Checking a type",
                "Use type(value) to ask Python what type a value has."
            ),
        ],
        "example": 'name = "Azhar"\nage = 20\nheight = 5.9\nactive = True\n\nprint(type(name))\nprint(type(age))\nprint(type(height))\nprint(type(active))',
        "task": "Create an integer variable and print its type.",
        "hint": "Create a number such as age = 20, then use print(type(age))."
    },

    {
        "title": "Input",
        "goal": "Learn how to receive information from the user.",
        "steps": [
            (
                "What is input()?",
                "input() pauses the program and waits for the user to type something."
            ),
            (
                "What does input() return?",
                "input() returns the user's response as a string."
            ),
            (
                "Storing input",
                "You can store the user's response inside a variable."
            ),
            (
                "Converting input",
                "Use int() when you need to convert numeric text into an integer."
            ),
        ],
        "example": 'name = input("Your name: ")\nprint("Hello", name)',
        "task": "Ask the user for their name and print a greeting.",
        "hint": 'Try: name = input("Your name: ")'
    },

    {
        "title": "Operators",
        "goal": "Use arithmetic, comparison and logical operators.",
        "steps": [
            (
                "Arithmetic operators",
                "Python supports +, -, *, /, //, %, and ** for common arithmetic operations."
            ),
            (
                "Comparison operators",
                "Comparison operators include ==, !=, >, <, >= and <=."
            ),
            (
                "Logical operators",
                "and, or and not let you combine or reverse logical conditions."
            ),
            (
                "Important",
                "= assigns a value. == compares two values."
            ),
        ],
        "example": 'a = 10\nb = 3\n\nprint(a + b)\nprint(a * b)\nprint(a > b)\nprint(a == b)',
        "task": "Create variables a and b and print their sum.",
        "hint": "Create a and b first, then use print(a + b)."
    },

    {
        "title": "Conditions",
        "goal": "Make decisions using if, elif and else.",
        "steps": [
            (
                "What is if?",
                "if lets your program execute code only when a condition is true."
            ),
            (
                "What is a condition?",
                "A condition is an expression that produces True or False."
            ),
            (
                "What is indentation?",
                "Indented lines belong to the block controlled by if, elif or else. Python uses indentation to define blocks of code."
            ),
            (
                "What is else?",
                "else runs when the previous condition is false."
            ),
            (
                "What is elif?",
                "elif lets you test another condition when the previous condition was false."
            ),
        ],
        "example": 'age = 18\n\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")',
        "task": "Print 'Adult' when age is 18 or above.",
        "hint": "Use if age >= 18: followed by an indented print()."
    },

    {
        "title": "for Loops",
        "goal": "Repeat code using for and range().",
        "steps": [
            (
                "What is a loop?",
                "A loop repeats a block of code."
            ),
            (
                "What is for?",
                "A for loop goes through items or values one at a time."
            ),
            (
                "What is range()?",
                "range() generates a sequence of numbers."
            ),
            (
                "Indentation",
                "The indented code under a for statement is repeated."
            ),
        ],
        "example": 'for i in range(1, 6):\n    print(i)',
        "task": "Print numbers 1 through 5 using a for loop.",
        "hint": "Use for i in range(1, 6): and print(i) inside the loop."
    },

    {
        "title": "while Loops",
        "goal": "Repeat code while a condition remains true.",
        "steps": [
            (
                "What is while?",
                "A while loop repeats code as long as its condition is true."
            ),
            (
                "Changing the condition",
                "You normally change a variable inside the loop so the condition eventually becomes false."
            ),
            (
                "Infinite loops",
                "If the condition never becomes false, the loop may continue indefinitely."
            ),
        ],
        "example": 'count = 0\n\nwhile count < 3:\n    print(count)\n    count += 1',
        "task": "Use a while loop to print 0, 1 and 2.",
        "hint": "Start count at 0 and increase it inside the loop."
    },

    {
        "title": "Lists",
        "goal": "Store multiple ordered values in a list.",
        "steps": [
            (
                "What is a list?",
                "A list stores multiple values in an ordered collection."
            ),
            (
                "Creating a list",
                "Lists use square brackets: [item1, item2, item3]."
            ),
            (
                "Indexing",
                "Python starts list indexes at 0. The first item is index 0."
            ),
            (
                "Changing a list",
                "Lists are mutable, which means their contents can be changed."
            ),
        ],
        "example": 'skills = ["Python", "Linux", "AI"]\nprint(skills[0])',
        "task": "Create a list of three skills and print the second item.",
        "hint": "The second item has index 1."
    },

    {
        "title": "Tuples & Sets",
        "goal": "Understand tuples and unique collections.",
        "steps": [
            (
                "What is a tuple?",
                "A tuple is an ordered collection that cannot normally be changed after creation."
            ),
            (
                "Tuple syntax",
                "Tuples are commonly written using parentheses."
            ),
            (
                "What is a set?",
                "A set stores unique values and automatically removes duplicates."
            ),
            (
                "Set syntax",
                "Sets are commonly created using curly braces."
            ),
        ],
        "example": 'items = {1, 2, 2, 3}\nprint(items)',
        "task": "Create a set containing 1, 2, 2, 3 and print it.",
        "hint": "Python will automatically keep only unique values."
    },

    {
        "title": "Dictionaries",
        "goal": "Store data using key-value pairs.",
        "steps": [
            (
                "What is a dictionary?",
                "A dictionary stores information as key-value pairs."
            ),
            (
                "Keys",
                "A key identifies a value."
            ),
            (
                "Values",
                "A value is the information stored under a key."
            ),
            (
                "Accessing values",
                "Use dictionary[key] to access a value."
            ),
        ],
        "example": 'user = {"name": "Azhar", "level": "beginner"}\nprint(user["name"])',
        "task": "Create a dictionary with name and age and print the name.",
        "hint": 'Try: user = {"name": "Azhar", "age": 20}'
    },

    {
        "title": "Functions",
        "goal": "Create reusable blocks of code.",
        "steps": [
            (
                "What is a function?",
                "A function is a reusable block of code designed to perform a task."
            ),
            (
                "def",
                "Use def to define a function."
            ),
            (
                "Parameters",
                "Parameters allow a function to receive information."
            ),
            (
                "return",
                "return sends a value back from a function."
            ),
        ],
        "example": 'def greet(name):\n    return "Hello " + name\n\nprint(greet("Azhar"))',
        "task": "Write a greet(name) function that returns a greeting.",
        "hint": 'Start with: def greet(name):'
    },

    {
        "title": "Function Arguments & Scope",
        "goal": "Understand arguments, defaults and variable scope.",
        "steps": [
            (
                "Arguments",
                "Arguments are values passed into a function when it is called."
            ),
            (
                "Default arguments",
                "A parameter can have a default value."
            ),
            (
                "Local variables",
                "Variables created inside a function are normally local to that function."
            ),
            (
                "Global variables",
                "Variables created outside functions can have a wider scope."
            ),
        ],
        "example": 'def add(a, b=0):\n    return a + b\n\nprint(add(5, 7))',
        "task": "Create a function that accepts two numbers and returns their sum.",
        "hint": "Use two parameters and return their addition."
    },

    {
        "title": "Modules",
        "goal": "Use modules to organize and reuse Python code.",
        "steps": [
            (
                "What is a module?",
                "A module is a Python file or library containing reusable code."
            ),
            (
                "import",
                "Use import to load a module."
            ),
            (
                "Standard library",
                "Python includes many useful modules in its standard library."
            ),
        ],
        "example": 'import math\nprint(math.sqrt(25))',
        "task": "Import the math module and calculate the square root of 64.",
        "hint": "Use math.sqrt(64)."
    },

    {
        "title": "File Handling",
        "goal": "Read from and write to files.",
        "steps": [
            (
                "Opening a file",
                "Use open() to work with a file."
            ),
            (
                "Write mode",
                'The "w" mode lets you write to a file.'
            ),
            (
                "Read mode",
                'The "r" mode lets you read a file.'
            ),
            (
                "with",
                "The with statement helps manage the file safely and closes it automatically."
            ),
        ],
        "example": 'with open("demo.txt", "w") as f:\n    f.write("Hello Python")',
        "task": "Create a file called practice.txt and write a short message into it.",
        "hint": 'Use open("practice.txt", "w").'
    },

    {
        "title": "Exceptions",
        "goal": "Handle expected runtime errors with try and except.",
        "steps": [
            (
                "What is an exception?",
                "An exception is an error that occurs while a program is running."
            ),
            (
                "try",
                "Put code that may fail inside a try block."
            ),
            (
                "except",
                "Use except to handle a specific error."
            ),
            (
                "Why handle errors?",
                "Error handling can make programs more reliable and user-friendly."
            ),
        ],
        "example": 'try:\n    number = int("10")\n    print(number)\nexcept ValueError:\n    print("Invalid number")',
        "task": "Safely convert a string into an integer using try and except.",
        "hint": "Handle ValueError."
    },

    {
        "title": "Comprehensions",
        "goal": "Create collections using concise expressions.",
        "steps": [
            (
                "What is a comprehension?",
                "A comprehension is a compact way to create a collection from another iterable."
            ),
            (
                "List comprehension",
                "List comprehensions commonly contain an expression followed by a for clause."
            ),
            (
                "Readability",
                "Use comprehensions when they make code clearer, not merely shorter."
            ),
        ],
        "example": 'squares = [x * x for x in range(5)]\nprint(squares)',
        "task": "Create a list containing the squares of numbers 0 through 5.",
        "hint": "Use a list comprehension with range(6)."
    },

    {
        "title": "OOP Basics",
        "goal": "Understand classes, objects and methods.",
        "steps": [
            (
                "What is a class?",
                "A class is a blueprint for creating objects."
            ),
            (
                "What is an object?",
                "An object is an instance created from a class."
            ),
            (
                "__init__",
                "__init__ is commonly used to initialize an object's attributes."
            ),
            (
                "self",
                "self refers to the current object instance inside instance methods."
            ),
        ],
        "example": 'class User:\n    def __init__(self, name):\n        self.name = name\n\nu = User("Azhar")\nprint(u.name)',
        "task": "Create a simple class with one attribute and print that attribute.",
        "hint": "Create a class called User with a name attribute."
    },

    {
        "title": "Inheritance",
        "goal": "Reuse and extend behavior between classes.",
        "steps": [
            (
                "What is inheritance?",
                "Inheritance allows one class to reuse behavior from another class."
            ),
            (
                "Parent class",
                "The class being inherited from is commonly called the parent or base class."
            ),
            (
                "Child class",
                "The class that inherits is commonly called the child or derived class."
            ),
            (
                "pass",
                "pass can be used when a class or block currently needs no additional statements."
            ),
        ],
        "example": 'class Animal:\n    def speak(self):\n        print("sound")\n\nclass Dog(Animal):\n    pass\n\nDog().speak()',
        "task": "Create a parent class and a child class that inherits a method.",
        "hint": "Make Dog inherit from Animal."
    },

    {
        "title": "Virtual Environments",
        "goal": "Isolate dependencies for Python projects.",
        "steps": [
            (
                "Why virtual environments?",
                "A virtual environment keeps project dependencies separate from other Python projects."
            ),
            (
                "Creating one",
                "Python can create a virtual environment using the venv module."
            ),
            (
                "Activating one",
                "Activation changes the shell environment so Python packages are installed into that environment."
            ),
            (
                "Project isolation",
                "Different projects can use different package versions."
            ),
        ],
        "example": "python3 -m venv .venv",
        "task": "Create a virtual environment named .venv.",
        "hint": "Use: python3 -m venv .venv"
    },

    {
        "title": "JSON & APIs",
        "goal": "Understand structured data and basic HTTP API concepts.",
        "steps": [
            (
                "What is JSON?",
                "JSON is a common text format for representing structured data."
            ),
            (
                "Objects",
                "JSON objects use key-value pairs."
            ),
            (
                "Python and JSON",
                "Python's json module can convert between Python data and JSON."
            ),
            (
                "What is an API?",
                "An API is an interface that allows software systems to communicate with each other."
            ),
        ],
        "example": 'import json\n\ndata = {"name": "Azhar", "active": True}\nprint(json.dumps(data))',
        "task": "Create a Python dictionary and convert it into JSON text.",
        "hint": "Use json.dumps()."
    },

    {
        "title": "Testing",
        "goal": "Verify that your code behaves correctly.",
        "steps": [
            (
                "Why test code?",
                "Tests help detect mistakes and prevent regressions."
            ),
            (
                "assert",
                "assert checks whether a condition is true."
            ),
            (
                "Expected behavior",
                "A good test describes behavior that should remain correct."
            ),
        ],
        "example": 'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5\nprint("Test passed")',
        "task": "Write a function and use assert to test its expected result.",
        "hint": "Create a small function such as add()."
    },

    {
        "title": "Debugging",
        "goal": "Learn a structured approach to finding and fixing errors.",
        "steps": [
            (
                "Read the error",
                "Start with the exception type and the line number."
            ),
            (
                "Reproduce the problem",
                "Run the smallest version of the code that still produces the error."
            ),
            (
                "Inspect values",
                "Use print() or a debugger to understand what your variables contain."
            ),
            (
                "Fix and test",
                "Make one change, run the code again, and verify the result."
            ),
        ],
        "example": 'numbers = [1, 2, 3]\nprint(numbers[1])',
        "task": "Write a small program and deliberately create a simple error, then fix it.",
        "hint": "Try creating and fixing an IndexError or NameError."
    },

    {
        "title": "Automation",
        "goal": "Automate useful local tasks with Python.",
        "steps": [
            (
                "What is automation?",
                "Automation means using software to perform repetitive tasks."
            ),
            (
                "Filesystem automation",
                "Python can inspect files and directories using modules such as pathlib."
            ),
            (
                "Safe automation",
                "Test automation carefully before allowing it to modify or delete files."
            ),
        ],
        "example": 'from pathlib import Path\n\nfor path in Path(".").iterdir():\n    print(path.name)',
        "task": "Write a program that lists files in the current directory.",
        "hint": "Use pathlib.Path."
    },

    {
        "title": "SQLite",
        "goal": "Store structured data in a local SQLite database.",
        "steps": [
            (
                "What is SQLite?",
                "SQLite is a lightweight database engine that stores data in a local database file."
            ),
            (
                "Connection",
                "Python's sqlite3 module can create and connect to SQLite databases."
            ),
            (
                "Tables",
                "Tables organize database records into columns and rows."
            ),
            (
                "Queries",
                "SQL statements can create, insert, update, delete and retrieve data."
            ),
        ],
        "example": 'import sqlite3\n\ncon = sqlite3.connect(":memory:")\ncon.execute("create table users(name text)")\ncon.execute("insert into users values (?)", ("Azhar",))\nprint(con.execute("select * from users").fetchall())',
        "task": "Create an SQLite table and insert one record.",
        "hint": "Use sqlite3.connect() and CREATE TABLE."
    },

    {
        "title": "Async Basics",
        "goal": "Understand async, await and asynchronous programming.",
        "steps": [
            (
                "What is asynchronous programming?",
                "Asynchronous programming allows a program to manage tasks that may spend time waiting."
            ),
            (
                "async",
                "The async keyword defines an asynchronous function."
            ),
            (
                "await",
                "await pauses an async function until an awaited operation is ready to continue."
            ),
            (
                "asyncio",
                "asyncio is Python's standard library framework for asynchronous programming."
            ),
        ],
        "example": 'import asyncio\n\nasync def main():\n    print("Hello async")\n\nasyncio.run(main())',
        "task": "Create and run a simple async function.",
        "hint": "Use async def and asyncio.run()."
    },

    {
        "title": "Advanced Python",
        "goal": "Explore decorators, generators and context managers.",
        "steps": [
            (
                "Decorators",
                "A decorator can modify or extend the behavior of a function."
            ),
            (
                "Generators",
                "Generators use yield to produce values lazily."
            ),
            (
                "Context managers",
                "Context managers manage setup and cleanup around a block of code."
            ),
            (
                "Why advanced features?",
                "These features can make larger Python programs more expressive and maintainable when used appropriately."
            ),
        ],
        "example": 'def decorator(fn):\n    def wrapper():\n        print("Before")\n        fn()\n    return wrapper\n\n@decorator\ndef hello():\n    print("Hello")\n\nhello()',
        "task": "Create a simple decorator that prints a message before a function runs.",
        "hint": "Create a decorator that accepts a function."
    },

    {
        "title": "Security-Focused Python",
        "goal": "Practice safe, defensive and security-aware Python programming.",
        "steps": [
            (
                "Secure coding",
                "Secure coding means designing software to reduce common security risks."
            ),
            (
                "Randomness",
                "Use the secrets module when generating security-sensitive random values."
            ),
            (
                "Input validation",
                "Validate input before using it in security-sensitive operations."
            ),
            (
                "Authorization",
                "Only test systems and data that you own or are explicitly authorized to test."
            ),
        ],
        "example": 'import secrets\n\ntoken = secrets.token_hex(8)\nprint(token)',
        "task": "Generate a secure random hexadecimal token using Python.",
        "hint": "Use secrets.token_hex()."
    },

    {
        "title": "Project Challenge",
        "goal": "Combine multiple Python concepts in a practical CLI project.",
        "steps": [
            (
                "Choose a problem",
                "Build something useful that solves a small real-world problem."
            ),
            (
                "Plan",
                "Write down the inputs, outputs and main features before coding."
            ),
            (
                "Build",
                "Create the program step by step instead of writing everything at once."
            ),
            (
                "Test",
                "Run different inputs and fix problems you discover."
            ),
        ],
        "example": 'print("Build something useful!")',
        "task": "Build a small command-line Python application.",
        "hint": "Good ideas include a calculator, quiz, notes app or task manager."
    },

    {
        "title": "Final Project",
        "goal": "Plan, build, test and improve a complete Python project.",
        "steps": [
            (
                "Project planning",
                "Define the problem your project will solve."
            ),
            (
                "Architecture",
                "Break the project into small functions, classes or modules."
            ),
            (
                "Implementation",
                "Build one feature at a time and test each feature."
            ),
            (
                "Testing",
                "Test normal inputs, invalid inputs and edge cases."
            ),
            (
                "Documentation",
                "Explain how the project works and how another person can run it."
            ),
        ],
        "example": 'print("Your Python journey starts here!")',
        "task": "Plan and build your own complete Python project.",
        "hint": "Use everything you have learned so far."
    },
]


# ============================================================
# CHALLENGES
# ============================================================

CHALLENGES = {
    1: 'Print your name and the words: "I am learning Python."',
    2: "Create a variable called city and print it.",
    3: "Create an integer variable and print its type.",
    4: "Ask the user for their name and print a greeting.",
    5: "Create variables a and b and print their sum.",
    6: "Print 'Adult' when age is 18 or above.",
    7: "Print numbers 1 through 5 using a for loop.",
    8: "Use a while loop to print 0, 1 and 2.",
    9: "Create a list of three skills and print the second item.",
    10: "Create a set containing 1, 2, 2, 3 and print it.",
    11: "Create a dictionary with name and age and print the name.",
    12: "Write a greet(name) function that returns a greeting.",
}


# ============================================================
# AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """You are HCO PythonTutor, an interactive Python teacher for
Termux and Linux.

Teach Python from absolute beginner to advanced level.

Assume the student may know nothing about programming.

Always explain new syntax before asking the student to use it.

When teaching:
- Explain every important symbol and keyword.
- Explain what the code does line by line when appropriate.
- Explain why the syntax is used.
- Give a simple example.
- Then give a small practice task.
- Prefer hints and guided reasoning before complete solutions.
- If the student provides an error, explain the error clearly.
- Do not pretend to execute code. The local HCO PythonTutor executes Python.
- Encourage the student to try again after mistakes.

For cybersecurity examples, stay legal, authorized, defensive and educational.
Do not provide instructions for unauthorized access, malware, credential theft,
or attacks against real systems."""


# ============================================================
# CLEAR TERMINAL
# ============================================================

def clear():
    os.system("clear")


# ============================================================
# HCO ASCII LOGO
# ============================================================

def logo():
    print(f"{CYAN}{BOLD}")

    print("██╗  ██╗ ██████╗  ██████╗ ")
    print("██║  ██║██╔════╝ ██╔═══██╗")
    print("███████║██║      ██║   ██║")
    print("██╔══██║██║      ██║   ██║")
    print("██║  ██║╚██████╗ ╚██████╔╝")
    print("╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ")

    print()
    print("       HCO PYTHON TUTOR")
    print(f"{RESET}")

    print(
        f"{MAGENTA}{BOLD}"
        "       by Azhar • HCO Team"
        f"{RESET}"
    )

    print()


# ============================================================
# OPEN YOUTUBE
# ============================================================

def open_youtube():

    commands = [
        ["termux-open-url", YOUTUBE_URL],
        [
            "am",
            "start",
            "-a",
            "android.intent.action.VIEW",
            YOUTUBE_URL,
        ],
        ["xdg-open", YOUTUBE_URL],
    ]

    for command in commands:

        try:

            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if result.returncode == 0:
                return True

        except Exception:
            pass

    return False


# ============================================================
# STARTUP
# ============================================================

def startup():

    clear()

    print(f"{RED}{BOLD}")

    print(
        "╔══════════════════════════════════════════════════════════╗"
    )

    print(
        "║                 🐍 HCO PYTHONTUTOR 🐍                  ║"
    )

    print(
        "╚══════════════════════════════════════════════════════════╝"
    )

    print(f"{RESET}\n")

    print(
        f"{YELLOW}{BOLD}"
        "Since you are learning Python for FREE using "
        "Hackers Colony's Free Tool,"
        f"{RESET}"
    )

    print(
        f"{WHITE}"
        "it's a request to please subscribe and click on "
        "the Bell 🔔 icon to support us."
        f"{RESET}\n"
    )

    print(
        f"{CYAN}{BOLD}"
        "📺 Hackers Colony Tech"
        f"{RESET}"
    )

    print(
        f"{CYAN}"
        f"{YOUTUBE_URL}"
        f"{RESET}\n"
    )

    print(
        f"{GREEN}{BOLD}"
        "Now Termux will redirect you to YouTube App in:"
        f"{RESET}\n"
    )

    for number in range(9, 0, -1):

        print(
            f"{YELLOW}{BOLD}"
            f"                         {number}"
            f"{RESET}"
        )

        time.sleep(1)

    print(
        f"\n{GREEN}{BOLD}"
        "📱 Opening Hackers Colony Tech..."
        f"{RESET}"
    )

    time.sleep(0.7)

    if not open_youtube():

        print(
            f"{RED}"
            "⚠️ Could not open YouTube automatically."
            f"{RESET}"
        )

        print(
            f"{CYAN}"
            f"{YOUTUBE_URL}"
            f"{RESET}"
        )

    print()

    input(
        f"{CYAN}{BOLD}"
        "↩️ Come back here and press ENTER to continue..."
        f"{RESET}"
    )


# ============================================================
# LOAD PROGRESS
# ============================================================

def load_progress():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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

        data = json.loads(
            PROGRESS_FILE.read_text(
                encoding="utf-8"
            )
        )

        default.update(data)

        return default

    except Exception:

        return default


# ============================================================
# SAVE PROGRESS
# ============================================================

def save_progress(progress):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    PROGRESS_FILE.write_text(
        json.dumps(
            progress,
            indent=2
        ),
        encoding="utf-8"
    )


# ============================================================
# GET OPENROUTER API KEY
# ============================================================

def get_api_key():

    clear()

    logo()

    print(
        f"{GREEN}{BOLD}"
        "🔐 AI TUTOR SETUP"
        f"{RESET}\n"
    )

    print(
        "HCO PythonTutor uses your own OpenRouter API key "
        "for the AI Tutor."
    )

    print(
        "The key is entered locally and is not included "
        "in the source code."
    )

    print()

    while True:

        try:

            key = getpass.getpass(
                f"{CYAN}{BOLD}"
                "OpenRouter API Key > "
                f"{RESET}"
            ).strip()

        except (KeyboardInterrupt, EOFError):

            print("\nCancelled.")
            sys.exit(1)

        if key:
            return key

        print(
            f"{RED}"
            "❌ API key cannot be empty."
            f"{RESET}"
        )


# ============================================================
# ASK AI
# ============================================================

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
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        },

        timeout=90,
    )

    try:

        data = response.json()

    except ValueError:

        raise RuntimeError(
            f"HTTP {response.status_code}: "
            "Invalid API response"
        )

    if response.status_code != 200:

        raise RuntimeError(
            f"API error ({response.status_code}): "
            f"{data.get('error', data)}"
        )

    try:

        return data["choices"][0]["message"]["content"]

    except (
        KeyError,
        IndexError,
        TypeError,
    ):

        raise RuntimeError(
            "Unexpected response format from OpenRouter."
        )


# ============================================================
# RUN LOCAL PYTHON CODE
# ============================================================

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

            return (
                output
                if output
                else
                "✅ Code ran successfully with no output."
            )

        return (
            (output + "\n" if output else "")
            + errors
        )

    except subprocess.TimeoutExpired:

        return (
            f"⏱️ Execution stopped after "
            f"{timeout} seconds."
        )

    except Exception as error:

        return f"Execution error: {error}"


# ============================================================
# MULTI-LINE CODE INPUT
# ============================================================

def multiline_input():

    print()

    print(
        f"{YELLOW}{BOLD}"
        "How to enter code:"
        f"{RESET}"
    )

    print(
        "1. Type only your Python code."
    )

    print(
        "2. Do NOT type >>> or ... ."
    )

    print(
        "3. When your program is complete, type END "
        "alone on a new line."
    )

    print()

    lines = []

    while True:

        try:

            if not lines:
                line = input(">>> ")
            else:
                line = input("... ")

        except (KeyboardInterrupt, EOFError):

            return ""

        if line.strip() == "END":

            return "\n".join(lines)

        lines.append(line)


# ============================================================
# PROGRESS BAR
# ============================================================

def progress_bar(progress):

    total = len(LESSONS)

    completed = len(
        progress.get(
            "completed_lessons",
            []
        )
    )

    width = 28

    filled = int(
        width * completed / total
    )

    return (
        f"{GREEN}"
        f"{'█' * filled}"
        f"{BLUE}"
        f"{'░' * (width - filled)}"
        f"{RESET} "
        f"{completed}/{total}"
    )


# ============================================================
# MARK LESSON COMPLETE
# ============================================================

def mark_lesson_complete(progress, number):

    completed = progress.setdefault(
        "completed_lessons",
        []
    )

    if number not in completed:

        completed.append(number)
        completed.sort()

    progress["current_lesson"] = min(
        number + 1,
        len(LESSONS)
    )

    save_progress(progress)


# ============================================================
# DISPLAY LESSON STEPS
# ============================================================

def display_lesson(lesson, number):

    clear()

    logo()

    print(
        f"{CYAN}{BOLD}"
        f"📚 LESSON {number:02d} — "
        f"{lesson['title']}"
        f"{RESET}\n"
    )

    print(
        f"{YELLOW}{BOLD}"
        "🎯 TODAY'S GOAL"
        f"{RESET}"
    )

    print(
        lesson["goal"]
    )

    print()

    print(
        f"{MAGENTA}{BOLD}"
        "📖 STEP-BY-STEP EXPLANATION"
        f"{RESET}\n"
    )

    for index, (heading, explanation) in enumerate(
        lesson["steps"],
        1
    ):

        print(
            f"{CYAN}{BOLD}"
            f"Step {index}: {heading}"
            f"{RESET}"
        )

        print(
            f"{WHITE}"
            f"{explanation}"
            f"{RESET}\n"
        )

    print(
        f"{YELLOW}{BOLD}"
        "💻 EXAMPLE"
        f"{RESET}\n"
    )

    print(
        f"{GREEN}"
        f"{lesson['example']}"
        f"{RESET}"
    )

    print()

    print(
        f"{BLUE}{BOLD}"
        "▶ Example result:"
        f"{RESET}"
    )

    example_output = run_python(
        lesson["example"]
    )

    print(
        f"{WHITE}"
        f"{example_output}"
        f"{RESET}"
    )

    print()

    print(
        f"{MAGENTA}{BOLD}"
        "🎯 YOUR PRACTICE TASK"
        f"{RESET}"
    )

    print(
        lesson["task"]
    )

    print()

    print(
        f"{YELLOW}"
        "💡 Hint:"
        f"{RESET}"
    )

    print(
        lesson["hint"]
    )

    print()

    input(
        f"{CYAN}{BOLD}"
        "Press ENTER when you are ready to write your code..."
        f"{RESET}"
    )


# ============================================================
# LEARN STEP-BY-STEP
# ============================================================

def learn_step_by_step(progress):

    number = min(
        max(
            progress.get(
                "current_lesson",
                1
            ),
            1
        ),
        len(LESSONS)
    )

    lesson = LESSONS[number - 1]

    display_lesson(
        lesson,
        number
    )

    print()

    print(
        f"{YELLOW}{BOLD}"
        "Now write your solution."
        f"{RESET}"
    )

    print(
        "Remember: type only Python code."
    )

    print(
        "When finished, type END on a separate line."
    )

    code = multiline_input()

    if not code.strip():
        return

    output = run_python(code)

    print(
        f"\n{YELLOW}{BOLD}"
        "▶ YOUR OUTPUT"
        f"{RESET}\n"
    )

    print(
        f"{WHITE}"
        f"{output}"
        f"{RESET}"
    )

    if (
        "SyntaxError:" in output
        or
        "Traceback" in output
    ):

        print()

        print(
            f"{RED}{BOLD}"
            "❌ Something needs fixing."
            f"{RESET}"
        )

        print(
            "Read the error carefully."
        )

        print(
            "You can use Ask AI Tutor for a guided hint."
        )

        print()

        input(
            "Press ENTER to return..."
        )

        return

    print()

    print(
        f"{GREEN}{BOLD}"
        "✅ Your code executed successfully!"
        f"{RESET}"
    )

    mark_lesson_complete(
        progress,
        number
    )

    print()

    print(
        f"{GREEN}"
        "🎉 Lesson completed!"
        f"{RESET}"
    )

    if number < len(LESSONS):

        print(
            f"{CYAN}"
            f"Next lesson: "
            f"{LESSONS[number][ 'title' ]}"
            f"{RESET}"
        )

    else:

        print(
            f"{MAGENTA}{BOLD}"
            "🏆 You completed the Python roadmap!"
            f"{RESET}"
        )

    input(
        "\nPress ENTER..."
    )


# ============================================================
# PRACTICE LAB
# ============================================================

def practice_lab():

    clear()

    logo()

    print(
        f"{CYAN}{BOLD}"
        "🧪 PRACTICE LAB"
        f"{RESET}\n"
    )

    print(
        "This is your free coding playground."
    )

    print(
        "Write Python code and run it locally."
    )

    print(
        "Type END alone on a new line when finished."
    )

    print()

    code = multiline_input()

    if code.strip():

        print(
            f"\n{YELLOW}{BOLD}"
            "▶ OUTPUT"
            f"{RESET}\n"
        )

        print(
            run_python(code)
        )

    input(
        "\nPress ENTER to return..."
    )


# ============================================================
# CODING CHALLENGE
# ============================================================

def challenge_mode(progress):

    level = min(
        max(
            progress.get(
                "current_lesson",
                1
            ),
            1
        ),
        len(LESSONS)
    )

    lesson = LESSONS[level - 1]

    task = CHALLENGES.get(
        level,
        lesson["task"]
    )

    clear()

    logo()

    print(
        f"{MAGENTA}{BOLD}"
        f"🎯 CODING CHALLENGE — "
        f"{lesson['title']}"
        f"{RESET}\n"
    )

    print(
        f"{YELLOW}{BOLD}"
        "Challenge:"
        f"{RESET}"
    )

    print(task)

    print()

    print(
        "Write your solution."
    )

    print(
        "Type END alone on a new line when finished."
    )

    code = multiline_input()

    if not code.strip():
        return

    output = run_python(code)

    print(
        f"\n{YELLOW}{BOLD}"
        "▶ OUTPUT"
        f"{RESET}\n"
    )

    print(output)

    if (
        "SyntaxError:" not in output
        and
        "Traceback" not in output
    ):

        progress["completed_challenges"] = (
            progress.get(
                "completed_challenges",
                0
            ) + 1
        )

        save_progress(progress)

        print()

        print(
            f"{GREEN}{BOLD}"
            "🎉 Challenge submitted successfully!"
            f"{RESET}"
        )

    else:

        print()

        print(
            f"{RED}{BOLD}"
            "❌ Fix the error and try again."
            f"{RESET}"
        )

    input(
        "\nPress ENTER..."
    )


# ============================================================
# AI TUTOR
# ============================================================

def ai_tutor(api_key, progress):

    clear()

    logo()

    print(
        f"{BLUE}{BOLD}"
        "🤖 ASK HCO PYTHON TUTOR"
        f"{RESET}\n"
    )

    print(
        "Ask about Python concepts, errors, code, "
        "projects or learning strategy."
    )

    print(
        "For debugging, include your code and "
        "the error message when possible."
    )

    print()

    try:

        question = input(
            f"{CYAN}"
            "Your question > "
            f"{RESET}"
        ).strip()

    except (KeyboardInterrupt, EOFError):

        return

    if not question:
        return

    current = progress.get(
        "current_lesson",
        1
    )

    lesson_title = LESSONS[
        current - 1
    ]["title"]

    context = (
        f"The student is currently on lesson "
        f"{current} of {len(LESSONS)}: "
        f"{lesson_title}.\n"
        "Teach at the student's level."
    )

    print(
        f"\n{YELLOW}"
        "⏳ AI Tutor is thinking..."
        f"{RESET}"
    )

    try:

        answer = ask_ai(
            api_key,
            context
            + "\n\nStudent question:\n"
            + question
        )

        print(
            f"\n{GREEN}{BOLD}"
            "🤖 HCO PYTHONTUTOR"
            f"{RESET}\n"
        )

        print(answer)

    except Exception as error:

        print(
            f"{RED}"
            f"❌ {error}"
            f"{RESET}"
        )

    input(
        "\nPress ENTER..."
    )


# ============================================================
# DAILY 10-MINUTE LEARNING
# ============================================================

def daily_10_minutes(progress):

    number = min(
        max(
            progress.get(
                "current_lesson",
                1
            ),
            1
        ),
        len(LESSONS)
    )

    lesson = LESSONS[number - 1]

    clear()

    logo()

    print(
        f"{YELLOW}{BOLD}"
        "🕐 DAILY 10-MINUTE PYTHON"
        f"{RESET}\n"
    )

    print(
        f"{CYAN}{BOLD}"
        f"Today's focus: {lesson['title']}"
        f"{RESET}"
    )

    print(
        "Goal: understand → practice → run → improve"
    )

    print()

    print(
        f"{MAGENTA}{BOLD}"
        "📖 QUICK LESSON"
        f"{RESET}"
    )

    print(
        lesson["goal"]
    )

    print()

    for index, (heading, explanation) in enumerate(
        lesson["steps"][:3],
        1
    ):

        print(
            f"{CYAN}"
            f"{index}. {heading}"
            f"{RESET}"
        )

        print(
            explanation
        )

        print()

    print(
        f"{YELLOW}{BOLD}"
        "💻 EXAMPLE"
        f"{RESET}"
    )

    print(
        f"{GREEN}"
        f"{lesson['example']}"
        f"{RESET}"
    )

    print()

    print(
        f"{MAGENTA}{BOLD}"
        "🎯 PRACTICE"
        f"{RESET}"
    )

    print(
        lesson["task"]
    )

    print()

    code = multiline_input()

    if not code.strip():
        return

    output = run_python(code)

    print(
        f"\n{YELLOW}{BOLD}"
        "▶ OUTPUT"
        f"{RESET}\n"
    )

    print(output)

    if (
        "SyntaxError:" not in output
        and
        "Traceback" not in output
    ):

        progress["daily_sessions"] = (
            progress.get(
                "daily_sessions",
                0
            ) + 1
        )

        mark_lesson_complete(
            progress,
            number
        )

        print()

        print(
            f"{GREEN}{BOLD}"
            "🎉 Daily session complete! +10 XP"
            f"{RESET}"
        )

        print(
            "Come back tomorrow for the next session."
        )

    else:

        print()

        print(
            f"{RED}"
            "Fix the error and repeat the practice."
            f"{RESET}"
        )

    input(
        "\nPress ENTER..."
    )


# ============================================================
# SHOW PROGRESS
# ============================================================

def show_progress(progress):

    clear()

    logo()

    print(
        f"{CYAN}{BOLD}"
        "📊 YOUR PYTHON PROGRESS"
        f"{RESET}\n"
    )

    print(
        f"Overall: "
        f"{progress_bar(progress)}"
    )

    print(
        f"🔥 Current streak: "
        f"{progress.get('streak', 0)}"
    )

    print(
        f"🧪 Challenges completed: "
        f"{progress.get('completed_challenges', 0)}"
    )

    print(
        f"🕐 Daily sessions: "
        f"{progress.get('daily_sessions', 0)}"
    )

    print()

    completed = set(
        progress.get(
            "completed_lessons",
            []
        )
    )

    for index, lesson in enumerate(
        LESSONS,
        1
    ):

        if index in completed:

            mark = (
                f"{GREEN}✓{RESET}"
            )

        else:

            mark = (
                f"{BLUE}○{RESET}"
            )

        print(
            f"{mark} "
            f"{index:02d}. "
            f"{lesson['title']}"
        )

    input(
        "\nPress ENTER..."
    )


# ============================================================
# MAIN MENU
# ============================================================

def main_menu(progress):

    while True:

        clear()

        logo()

        print(
            f"{YELLOW}{BOLD}"
            "🐍 Beginner → Advanced Python Learning"
            f"{RESET}"
        )

        print(
            f"Progress: "
            f"{progress_bar(progress)}\n"
        )

        print(
            f"{CYAN}[1]{RESET} "
            "📚 Learn Step-by-Step"
        )

        print(
            f"{GREEN}[2]{RESET} "
            "🕐 Daily 10-Minute Learning"
        )

        print(
            f"{MAGENTA}[3]{RESET} "
            "🧪 Practice Lab"
        )

        print(
            f"{BLUE}[4]{RESET} "
            "🎯 Coding Challenge"
        )

        print(
            f"{YELLOW}[5]{RESET} "
            "🤖 Ask AI Tutor"
        )

        print(
            f"{CYAN}[6]{RESET} "
            "📊 My Progress"
        )

        print(
            f"{RED}[0]{RESET} "
            "🚪 Exit"
        )

        print()

        try:

            choice = input(
                f"{MAGENTA}{BOLD}"
                "HCO PythonTutor > "
                f"{RESET}"
            ).strip()

        except (KeyboardInterrupt, EOFError):

            print(
                "\nGoodbye! 👋"
            )

            return

        if choice == "1":

            learn_step_by_step(
                progress
            )

        elif choice == "2":

            daily_10_minutes(
                progress
            )

        elif choice == "3":

            practice_lab()

        elif choice == "4":

            challenge_mode(
                progress
            )

        elif choice == "5":

            ai_tutor(
                API_KEY,
                progress
            )

        elif choice == "6":

            show_progress(
                progress
            )

        elif choice == "0":

            print()

            print(
                f"{GREEN}"
                "Keep learning. Keep building. 🐍🔥"
                f"{RESET}"
            )

            return

        else:

            input(
                f"\n{RED}"
                "❌ Invalid option. Press ENTER..."
                f"{RESET}"
            )


# ============================================================
# GLOBAL API KEY
# ============================================================

API_KEY = ""


# ============================================================
# MAIN
# ============================================================

def main():

    global API_KEY

    startup()

    API_KEY = get_api_key()

    progress = load_progress()

    clear()

    logo()

    print(
        f"{GREEN}{BOLD}"
        "🔓 HCO PYTHONTUTOR READY! 🔓"
        f"{RESET}"
    )

    print(
        "Learn Python from absolute beginner "
        "to advanced level."
    )

    print(
        "Learn → Write → Run → Fix → Challenge → Progress"
    )

    time.sleep(2)

    main_menu(
        progress
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
