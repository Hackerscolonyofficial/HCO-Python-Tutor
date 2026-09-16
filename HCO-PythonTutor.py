#!/usr/bin/env python3

import ast
import getpass
import json
import os
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import requests


# ============================================================
# HCO PYTHONTUTOR
# Interactive Python Learning Companion for Termux & Linux
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
# CURRICULUM
# Each lesson has explanation, examples, 10 exercises and
# a challenge. Exercises are checked by running the student's
# code plus lightweight task-specific checks where possible.
# ============================================================

LESSONS = [
    {
        "title": "Python & print()",
        "level": "Beginner",
        "goal": "Learn what Python is and write your first programs.",
        "concepts": [
            ("Python", "Python is a programming language. You write instructions and the Python interpreter executes them."),
            ("print()", "print() displays information on the screen."),
            ("Parentheses", "The parentheses pass information into a function."),
            ("Strings", 'Text is a string. Strings are commonly written inside quotes such as "Hello".'),
            ("Numbers", "Numbers such as 10 can be written without quotes."),
            ("Quotes", 'print("Azhar") prints text. print(Azhar) tries to use Azhar as a variable.'),
            ("Interactive prompts", "The >>> and ... prompts are displayed by the tutor. You do not type them."),
            ("END", "HCO PythonTutor uses END alone on a new line to finish a multi-line code submission."),
        ],
        "example": 'print("Hello, Hackers Colony!")',
        "exercises": [
            'Print "Hello".',
            'Print your name.',
            'Print "I am learning Python."',
            'Print two different messages on two lines.',
            'Print the number 100.',
            'Print your name and your favorite technology.',
            'Print "Python" three times using three print() statements.',
            'Print a sentence containing spaces.',
            'Print both text and a number using separate print() statements.',
            'Create a tiny program that prints your name, city, and "I am learning Python."',
        ],
        "challenge": 'Build a 3-line introduction program that prints your name, your city, and why you are learning Python.',
        "hints": [
            'Use print("Hello").',
            'Put text inside quotes.',
            'Use one print() statement for each line.',
        ],
    },
    {
        "title": "Variables",
        "level": "Beginner",
        "goal": "Store values in variables and use them later.",
        "concepts": [
            ("Variable", "A variable is a name that refers to a value."),
            ("Assignment", "The = operator assigns a value to a variable."),
            ("Variable names", "Use clear names such as name, age, city, or score."),
            ("Reusing values", "After assignment, use the variable name to access its value."),
            ("Updating values", "A variable can be assigned a new value later."),
            ("Naming rules", "Names cannot contain spaces and cannot start with a number."),
        ],
        "example": 'name = "Azhar"\ncity = "Kolkata"\nprint(name)\nprint(city)',
        "exercises": [
            'Create a variable called name and print it.',
            'Create a variable called city and print it.',
            'Create an age variable and print it.',
            'Create a score variable with 100 and print it.',
            'Create two variables and print both.',
            'Change the value of a variable and print the new value.',
            'Create name and city variables and print a sentence using them.',
            'Create length and width variables and print their product.',
            'Create a counter variable and increase it by 1.',
            'Create a profile using at least four variables and print them.',
        ],
        "challenge": "Build a small profile program using variables for name, age, city, and skill.",
        "hints": [
            'Assignment looks like: name = "Azhar".',
            'Use print(variable) to display a stored value.',
            'Remember that = assigns a value; == compares values.',
        ],
    },
    {
        "title": "Data Types",
        "level": "Beginner",
        "goal": "Understand strings, integers, floats, booleans and type().",
        "concepts": [
            ("String", 'Text such as "Python" is a string.'),
            ("Integer", "A whole number such as 20 is an integer."),
            ("Float", "A decimal number such as 3.14 is a float."),
            ("Boolean", "True and False are boolean values."),
            ("type()", "type(value) tells you the data type of a value."),
            ("Type conversion", "int(), float(), and str() convert compatible values."),
        ],
        "example": 'name = "Azhar"\nage = 20\nheight = 5.9\nactive = True\nprint(type(name))\nprint(type(age))\nprint(type(height))\nprint(type(active))',
        "exercises": [
            'Create a string and print its type.',
            'Create an integer and print its type.',
            'Create a float and print its type.',
            'Create a boolean and print its type.',
            'Print the types of four different values.',
            'Convert "25" into an integer and print it.',
            'Convert 10 into a float and print it.',
            'Convert 123 into a string and print it.',
            'Create a small data record using different types.',
            'Print a value and its type together using separate print() calls.',
        ],
        "challenge": "Create a student profile using at least one string, integer, float, and boolean.",
        "hints": [
            "Use type(value).",
            'Remember: "25" is text, while 25 is an integer.',
            "Use int(), float(), or str() when conversion is needed.",
        ],
    },
    {
        "title": "Input",
        "level": "Beginner",
        "goal": "Receive information from the user and convert input when needed.",
        "concepts": [
            ("input()", "input() waits for the user to type a response."),
            ("Return value", "input() returns the entered value as a string."),
            ("Prompt text", 'input("Your name: ") displays a prompt.'),
            ("Storing input", "Assign input() to a variable."),
            ("Integer input", "Use int(input(...)) when a whole number is required."),
            ("Float input", "Use float(input(...)) when a decimal number is required."),
        ],
        "example": 'name = input("Your name: ")\nprint("Hello", name)',
        "exercises": [
            "Ask the user for their name and print it.",
            "Ask for a city and print it.",
            "Ask for a favorite programming language and print it.",
            "Ask for age and convert it to an integer.",
            "Ask for two numbers and print their sum.",
            "Ask for name and city and print both.",
            "Ask for a number and print its square.",
            "Ask for a year and calculate the next year.",
            "Ask for a price and quantity and calculate the total.",
            "Build an interactive introduction program using three inputs.",
        ],
        "challenge": "Build a simple interactive profile program that asks for name, city, age, and favorite skill.",
        "hints": [
            'Start with: name = input("Your name: ")',
            "Remember that input() returns text.",
            "Use int() for whole-number calculations.",
        ],
    },
    {
        "title": "Operators",
        "level": "Beginner",
        "goal": "Use arithmetic, comparison and logical operators.",
        "concepts": [
            ("Arithmetic", "Use +, -, *, /, //, %, and ** for calculations."),
            ("Comparison", "Use ==, !=, >, <, >=, and <= to compare values."),
            ("Logical", "Use and, or, and not to combine conditions."),
            ("Assignment", "Use = to assign a value."),
            ("Equality", "Use == to compare two values."),
            ("Modulo", "% gives the remainder of a division."),
        ],
        "example": 'a = 10\nb = 3\nprint(a + b)\nprint(a * b)\nprint(a > b)\nprint(a == b)\nprint(a % b)',
        "exercises": [
            "Add two numbers.",
            "Subtract two numbers.",
            "Multiply two numbers.",
            "Divide two numbers.",
            "Find the remainder of two numbers.",
            "Calculate a number raised to a power.",
            "Compare two numbers using >.",
            "Compare two values using ==.",
            "Use and with two boolean conditions.",
            "Build a mini calculator for two numbers.",
        ],
        "challenge": "Build a two-number calculator supporting +, -, *, and /.",
        "hints": [
            "Use + for addition.",
            "Use == for comparison.",
            "Use % when you need a remainder.",
        ],
    },
    {
        "title": "Conditions",
        "level": "Beginner",
        "goal": "Make decisions with if, elif, else and indentation.",
        "concepts": [
            ("if", "if runs a block when its condition is True."),
            ("else", "else runs when the previous condition is False."),
            ("elif", "elif checks another condition."),
            ("Colon", "A colon starts the indented block after if, elif, or else."),
            ("Indentation", "Indented lines belong to the current block."),
            ("Comparison", "Conditions commonly use comparison operators."),
        ],
        "example": 'age = 18\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")',
        "exercises": [
            "Print Adult when age is 18 or above.",
            "Check whether a number is positive.",
            "Check whether a number is negative or zero.",
            "Check whether two numbers are equal.",
            "Print Pass when score is 40 or above.",
            "Create an if/else login message using a stored username.",
            "Use elif for three score ranges.",
            "Check whether a number is even or odd.",
            "Use two conditions with and.",
            "Build a simple age-category program.",
        ],
        "challenge": "Build a grade checker that prints a different message for several score ranges.",
        "hints": [
            "Start a condition with if.",
            "Remember the colon after the condition.",
            "The code inside the block must be indented.",
        ],
    },
    {
        "title": "for Loops",
        "level": "Beginner",
        "goal": "Repeat code using for and range().",
        "concepts": [
            ("Loop", "A loop repeats code."),
            ("for", "A for loop iterates over values."),
            ("range()", "range() produces a sequence of integers."),
            ("Loop variable", "The variable after for receives each value."),
            ("Indentation", "The indented block is repeated."),
        ],
        "example": 'for i in range(1, 6):\n    print(i)',
        "exercises": [
            "Print numbers 1 through 5.",
            "Print numbers 0 through 4.",
            "Print the word Python five times.",
            "Print even numbers from 2 to 10.",
            "Print odd numbers from 1 to 9.",
            "Calculate the sum of numbers 1 through 10.",
            "Loop through a list of three names.",
            "Print a multiplication table.",
            "Count down from 10 to 1.",
            "Build a small number-report program using a loop.",
        ],
        "challenge": "Build a multiplication table generator for a number chosen by the user.",
        "hints": [
            "Use range().",
            "Put repeated code inside the indented loop body.",
            "Use a loop variable such as i.",
        ],
    },
    {
        "title": "while Loops",
        "level": "Beginner",
        "goal": "Repeat code while a condition remains true.",
        "concepts": [
            ("while", "while repeats a block while its condition is True."),
            ("Counter", "A counter can control how many times a loop runs."),
            ("Update", "Change the loop variable so the loop can eventually stop."),
            ("Infinite loop", "A condition that never becomes false can create an infinite loop."),
        ],
        "example": 'count = 0\nwhile count < 3:\n    print(count)\n    count += 1',
        "exercises": [
            "Print 0, 1, and 2 with while.",
            "Count from 1 to 5.",
            "Count down from 5 to 1.",
            "Print a word three times.",
            "Calculate a running total.",
            "Ask for a password until the correct value is entered.",
            "Stop when the user enters quit.",
            "Create a simple menu loop.",
            "Use a counter to limit attempts.",
            "Build a number guessing loop.",
        ],
        "challenge": "Build a small menu that keeps running until the user chooses Exit.",
        "hints": [
            "Start with a variable before the loop.",
            "Update that variable inside the loop.",
            "Make sure there is a clear exit condition.",
        ],
    },
    {
        "title": "Lists",
        "level": "Beginner",
        "goal": "Store and manipulate ordered collections.",
        "concepts": [
            ("List", "A list stores multiple ordered values."),
            ("Square brackets", "Lists are written with square brackets."),
            ("Index", "Python list indexes start at 0."),
            ("append()", "append() adds an item to the end."),
            ("remove()", "remove() removes a matching value."),
            ("len()", "len() returns the number of items."),
        ],
        "example": 'skills = ["Python", "Linux", "AI"]\nprint(skills[0])\nskills.append("Git")\nprint(skills)',
        "exercises": [
            "Create a list of three names.",
            "Print the first item.",
            "Print the second item.",
            "Append a new item.",
            "Remove an item.",
            "Print the length of a list.",
            "Loop through a list.",
            "Create a list of numbers and calculate a sum.",
            "Sort a list of numbers.",
            "Build a simple shopping-list program.",
        ],
        "challenge": "Build a command-line shopping list with add, view, and remove operations.",
        "hints": [
            "The first item has index 0.",
            "Use append() to add an item.",
            "Use len() to count items.",
        ],
    },
    {
        "title": "Tuples & Sets",
        "level": "Beginner",
        "goal": "Understand immutable sequences and unique collections.",
        "concepts": [
            ("Tuple", "A tuple is an ordered collection that is normally immutable."),
            ("Tuple syntax", "Tuples are commonly written with parentheses."),
            ("Set", "A set stores unique values."),
            ("Duplicate removal", "Sets automatically remove duplicate values."),
            ("Membership", "Use in to test whether a value exists in a collection."),
        ],
        "example": 'items = {1, 2, 2, 3}\nprint(items)\ncolors = ("red", "green", "blue")\nprint(colors[0])',
        "exercises": [
            "Create a tuple of three colors.",
            "Print the first tuple item.",
            "Create a set with duplicate numbers.",
            "Print the set.",
            "Add an item to a set.",
            "Remove an item from a set.",
            "Check membership with in.",
            "Find the length of a set.",
            "Convert a list into a set.",
            "Build a unique-skills collector.",
        ],
        "challenge": "Build a small program that accepts several skills and displays only unique skills.",
        "hints": [
            "Sets use curly braces or set().",
            "Tuples are commonly written with parentheses.",
            "Use in for membership checks.",
        ],
    },
    {
        "title": "Dictionaries",
        "level": "Beginner",
        "goal": "Store information using key-value pairs.",
        "concepts": [
            ("Dictionary", "A dictionary stores key-value pairs."),
            ("Key", "A key identifies a value."),
            ("Value", "A value is the data stored under a key."),
            ("Access", "Use dictionary[key] to access a value."),
            ("Update", "Assign to an existing key to update its value."),
            ("get()", "get() can safely retrieve a value when a key may be missing."),
        ],
        "example": 'user = {"name": "Azhar", "level": "beginner"}\nprint(user["name"])\nuser["level"] = "intermediate"\nprint(user)',
        "exercises": [
            "Create a dictionary with name and age.",
            "Print the name.",
            "Add a city key.",
            "Update the age.",
            "Use get() to read a key.",
            "Loop through dictionary keys.",
            "Loop through key-value pairs.",
            "Create a dictionary of three scores.",
            "Calculate a total from dictionary values.",
            "Build a small contact record.",
        ],
        "challenge": "Build a simple contact-book program using a dictionary.",
        "hints": [
            'Use syntax like {"name": "Azhar"}.',
            "Access values with dictionary[key].",
            "Use items() when looping over key-value pairs.",
        ],
    },
    {
        "title": "Functions",
        "level": "Beginner",
        "goal": "Create reusable blocks of code.",
        "concepts": [
            ("def", "def starts a function definition."),
            ("Function name", "Choose a clear name describing the function's job."),
            ("Parameter", "A parameter is a named input to a function."),
            ("Call", "Use function_name() to call a function."),
            ("return", "return sends a value back to the caller."),
        ],
        "example": 'def greet(name):\n    return "Hello " + name\n\nprint(greet("Azhar"))',
        "exercises": [
            "Create a function that prints Hello.",
            "Create greet(name).",
            "Create add(a, b).",
            "Create a function that squares a number.",
            "Create a function that checks even/odd.",
            "Create a function with a default parameter.",
            "Return a string from a function.",
            "Call the same function three times.",
            "Create two helper functions.",
            "Build a mini calculator using functions.",
        ],
        "challenge": "Build a calculator where each operation is implemented as a separate function.",
        "hints": [
            "Start with def function_name(...):",
            "Indent the function body.",
            "Use return when the caller needs a result.",
        ],
    },
    {
        "title": "Function Arguments & Scope",
        "level": "Intermediate",
        "goal": "Understand arguments, defaults, *args, **kwargs and scope.",
        "concepts": [
            ("Positional arguments", "Arguments can be passed by position."),
            ("Keyword arguments", "Arguments can be passed by parameter name."),
            ("Defaults", "Parameters can have default values."),
            ("*args", "*args collects extra positional arguments."),
            ("**kwargs", "**kwargs collects extra keyword arguments."),
            ("Scope", "Scope determines where a variable can be accessed."),
        ],
        "example": 'def add(a, b=0):\n    return a + b\n\nprint(add(5, 7))\nprint(add(5))',
        "exercises": [
            "Create a function with two positional arguments.",
            "Call a function using keyword arguments.",
            "Create a function with a default value.",
            "Create a function using *args.",
            "Create a function using **kwargs.",
            "Write a function that returns the largest argument.",
            "Demonstrate a local variable.",
            "Write a function that calls another function.",
            "Create a configurable greeting function.",
            "Build a reusable utility module in one file.",
        ],
        "challenge": "Build a flexible report function that accepts a title, multiple values, and optional settings.",
        "hints": [
            "Default parameters look like name=value.",
            "*args is a tuple inside the function.",
            "**kwargs is a dictionary inside the function.",
        ],
    },
    {
        "title": "Modules",
        "level": "Intermediate",
        "goal": "Organize code and use Python modules.",
        "concepts": [
            ("Module", "A module is a Python file containing reusable code."),
            ("import", "import loads a module."),
            ("from", "from can import selected names."),
            ("Standard library", "Python includes many useful modules."),
            ("Your modules", "You can create your own .py files and import them."),
        ],
        "example": 'import math\nprint(math.sqrt(25))',
        "exercises": [
            "Import math.",
            "Use math.sqrt().",
            "Import random.",
            "Generate a random integer.",
            "Import pathlib.",
            "List files with pathlib.",
            "Import a specific function from a module.",
            "Create a helper module.",
            "Import your helper module.",
            "Build a two-file mini project.",
        ],
        "challenge": "Create a two-file Python project with a main program and a reusable utility module.",
        "hints": [
            "Use import module_name.",
            "Your custom module can be another .py file in the same directory.",
            "Keep reusable functions in the helper module.",
        ],
    },
    {
        "title": "File Handling",
        "level": "Intermediate",
        "goal": "Read, write and safely manage files.",
        "concepts": [
            ("open()", "open() creates a file object."),
            ("Modes", "Common modes include r for read, w for write, and a for append."),
            ("with", "with manages the file resource and closes it automatically."),
            ("read()", "read() returns file contents."),
            ("write()", "write() writes text to a file."),
            ("Path", "pathlib.Path provides a convenient modern path API."),
        ],
        "example": 'with open("demo.txt", "w") as f:\n    f.write("Hello Python")\n\nwith open("demo.txt", "r") as f:\n    print(f.read())',
        "exercises": [
            "Write text to a file.",
            "Read the file.",
            "Append another line.",
            "Count lines in a file.",
            "Count words in a file.",
            "Check whether a file exists.",
            "List files in the current directory.",
            "Read a file line by line.",
            "Copy text from one file to another.",
            "Build a simple notes file program.",
        ],
        "challenge": "Build a local notes manager that can add and view notes in a text file.",
        "hints": [
            'Use with open("file.txt", "w") as f:',
            "Use append mode a when you want to add data.",
            "pathlib.Path can check whether files exist.",
        ],
    },
    {
        "title": "Exceptions",
        "level": "Intermediate",
        "goal": "Handle expected errors with try, except, else and finally.",
        "concepts": [
            ("Exception", "An exception is an error raised while a program runs."),
            ("try", "Put code that may raise an expected exception inside try."),
            ("except", "Handle a specific exception in except."),
            ("else", "else runs when the try block succeeds."),
            ("finally", "finally runs whether an exception occurred or not."),
            ("raise", "raise lets your code deliberately signal an error."),
        ],
        "example": 'try:\n    number = int("hello")\nexcept ValueError:\n    print("Please enter a number.")',
        "exercises": [
            "Catch ValueError from int().",
            "Catch ZeroDivisionError.",
            "Handle invalid user input.",
            "Use else with try/except.",
            "Use finally.",
            "Raise ValueError for invalid data.",
            "Create a safe integer input function.",
            "Handle a missing file.",
            "Handle multiple expected exceptions.",
            "Build a robust calculator.",
        ],
        "challenge": "Build an input validator that keeps asking until valid numeric input is received.",
        "hints": [
            "Catch the specific exception you expect.",
            "Do not use bare except when a specific exception is appropriate.",
            "Use a loop when the user should retry.",
        ],
    },
    {
        "title": "Comprehensions",
        "level": "Intermediate",
        "goal": "Create collections concisely while keeping code readable.",
        "concepts": [
            ("List comprehension", "Build a list from an iterable using a compact expression."),
            ("Condition", "A comprehension can include a filtering condition."),
            ("Set comprehension", "The same idea can create sets."),
            ("Dictionary comprehension", "Comprehensions can create dictionaries."),
            ("Readability", "Shorter code is not always clearer; prefer readable expressions."),
        ],
        "example": 'squares = [x * x for x in range(6)]\nprint(squares)\nevens = [x for x in range(10) if x % 2 == 0]\nprint(evens)',
        "exercises": [
            "Create squares from 0 to 5.",
            "Create even numbers from 0 to 10.",
            "Convert words to uppercase.",
            "Filter words longer than four characters.",
            "Create a set of unique lengths.",
            "Create a dictionary of numbers and squares.",
            "Flatten a small nested list.",
            "Strip whitespace from words.",
            "Combine a filter and transformation.",
            "Rewrite a simple loop as a comprehension.",
        ],
        "challenge": "Build a data-cleaning script that filters and transforms a list of user-provided words.",
        "hints": [
            "Start with [expression for item in iterable].",
            "Add if condition for filtering.",
            "Keep complex logic in normal loops or helper functions.",
        ],
    },
    {
        "title": "OOP Basics",
        "level": "Intermediate",
        "goal": "Understand classes, objects, attributes and methods.",
        "concepts": [
            ("Class", "A class is a blueprint for creating objects."),
            ("Object", "An object is an instance of a class."),
            ("__init__", "__init__ commonly initializes object attributes."),
            ("self", "self refers to the current object instance."),
            ("Method", "A method is a function defined inside a class."),
            ("Attribute", "An attribute is data stored on an object."),
        ],
        "example": 'class User:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        return "Hello " + self.name\n\nu = User("Azhar")\nprint(u.greet())',
        "exercises": [
            "Create a simple class.",
            "Create an object from it.",
            "Add an attribute.",
            "Add a method.",
            "Use __init__.",
            "Create two objects with different data.",
            "Create a counter class.",
            "Create a simple BankAccount class.",
            "Add validation to a method.",
            "Build a small class-based program.",
        ],
        "challenge": "Build a BankAccount class with deposit, withdraw, and balance behavior.",
        "hints": [
            "Start with class ClassName:.",
            "Use self inside instance methods.",
            "Initialize attributes inside __init__.",
        ],
    },
    {
        "title": "Inheritance",
        "level": "Intermediate",
        "goal": "Reuse and extend behavior between classes.",
        "concepts": [
            ("Inheritance", "A child class can inherit behavior from a parent class."),
            ("Parent", "The base class provides reusable behavior."),
            ("Child", "The derived class can add or override behavior."),
            ("super()", "super() can call behavior from the parent class."),
            ("Override", "A child method can replace a parent implementation."),
        ],
        "example": 'class Animal:\n    def speak(self):\n        print("sound")\n\nclass Dog(Animal):\n    def speak(self):\n        print("woof")\n\nDog().speak()',
        "exercises": [
            "Create a parent class.",
            "Create a child class.",
            "Inherit a method.",
            "Override a method.",
            "Use super().",
            "Add a child-specific attribute.",
            "Create two child classes.",
            "Use polymorphic method calls.",
            "Build a simple vehicle hierarchy.",
            "Refactor duplicated behavior with inheritance.",
        ],
        "challenge": "Create a base Vehicle class and two specialized child classes with different behavior.",
        "hints": [
            "Use class Child(Parent):.",
            "Call super() when parent initialization or behavior is needed.",
            "Override only when the child really needs different behavior.",
        ],
    },
    {
        "title": "Virtual Environments",
        "level": "Intermediate",
        "goal": "Isolate project dependencies.",
        "concepts": [
            ("Why venv?", "Virtual environments keep project packages separate."),
            ("Create", "python3 -m venv .venv creates a virtual environment."),
            ("Activate", "Activation changes the shell environment to use the environment."),
            ("Packages", "Install project-specific packages inside the environment."),
            ("Requirements", "requirements.txt records dependencies for reproducible setup."),
        ],
        "example": "python3 -m venv .venv",
        "exercises": [
            "Create a .venv environment.",
            "Inspect the environment directory.",
            "Activate a virtual environment on Linux/Termux.",
            "Check the Python version.",
            "Install a small package.",
            "List installed packages.",
            "Create a requirements.txt file.",
            "Install from requirements.txt.",
            "Deactivate the environment.",
            "Explain why isolation is useful for a project.",
        ],
        "challenge": "Create a clean Python project environment and document its setup commands.",
        "hints": [
            "Create with: python3 -m venv .venv",
            "Activation commands depend on your shell.",
            "requirements.txt can be installed with pip install -r requirements.txt.",
        ],
    },
    {
        "title": "JSON & APIs",
        "level": "Intermediate",
        "goal": "Work with structured data and HTTP APIs.",
        "concepts": [
            ("JSON", "JSON is a common text format for structured data."),
            ("json.dumps", "Converts a Python object to JSON text."),
            ("json.loads", "Converts JSON text to a Python object."),
            ("API", "An API is an interface for software-to-software communication."),
            ("HTTP", "HTTP is commonly used to send requests to web APIs."),
            ("Status codes", "HTTP status codes communicate request results."),
        ],
        "example": 'import json\n\ndata = {"name": "Azhar", "active": True}\ntext = json.dumps(data)\nprint(text)\nprint(json.loads(text)["name"])',
        "exercises": [
            "Create a dictionary and convert it to JSON.",
            "Convert JSON text back to Python.",
            "Read a value from decoded JSON.",
            "Create a JSON list.",
            "Write JSON to a file.",
            "Read JSON from a file.",
            "Inspect an HTTP response status code.",
            "Send a request to a public API you are authorized to use.",
            "Handle API errors.",
            "Build a small JSON-backed data tool.",
        ],
        "challenge": "Build a small program that reads JSON data, validates it, and displays selected fields.",
        "hints": [
            "Use json.dumps() for Python → JSON text.",
            "Use json.loads() for JSON text → Python.",
            "Always handle network errors when making HTTP requests.",
        ],
    },
    {
        "title": "Testing",
        "level": "Intermediate",
        "goal": "Verify program behavior with tests and assertions.",
        "concepts": [
            ("Test", "A test checks whether software behaves as expected."),
            ("assert", "assert verifies that a condition is true."),
            ("Test cases", "Different inputs should cover normal and edge cases."),
            ("Regression", "Tests help detect when a change breaks existing behavior."),
            ("pytest", "pytest is a popular external Python testing framework."),
        ],
        "example": 'def add(a, b):\n    return a + b\n\nassert add(2, 3) == 5\nprint("Test passed")',
        "exercises": [
            "Test an addition function.",
            "Test a subtraction function.",
            "Test a string function.",
            "Test an even/odd function.",
            "Test an edge case.",
            "Write multiple assertions.",
            "Create a test function.",
            "Test invalid input behavior.",
            "Separate application code from tests.",
            "Run a small test suite.",
        ],
        "challenge": "Create a utility module and a test file containing at least five meaningful tests.",
        "hints": [
            "Use assert expected == actual.",
            "Include normal and edge cases.",
            "Keep tests focused on observable behavior.",
        ],
    },
    {
        "title": "Debugging",
        "level": "Intermediate",
        "goal": "Develop a systematic process for finding and fixing bugs.",
        "concepts": [
            ("Read traceback", "A traceback shows where an exception occurred."),
            ("Reproduce", "Reproduce the bug consistently before changing code."),
            ("Inspect", "Inspect variables and assumptions."),
            ("Small changes", "Change one thing at a time and retest."),
            ("Logging", "Logging can provide useful runtime information."),
        ],
        "example": 'numbers = [1, 2, 3]\nprint(numbers[1])',
        "exercises": [
            "Fix a NameError.",
            "Fix an IndexError.",
            "Fix a TypeError.",
            "Fix an indentation error.",
            "Fix a wrong variable value.",
            "Use print() to inspect state.",
            "Read a traceback and identify its line.",
            "Add logging to a small program.",
            "Create and fix a bug intentionally.",
            "Write a short debugging checklist.",
        ],
        "challenge": "Debug a deliberately broken mini-program and explain each fix.",
        "hints": [
            "Start with the exception type.",
            "Check the line named in the traceback.",
            "Reproduce the smallest version of the problem.",
        ],
    },
    {
        "title": "Automation",
        "level": "Intermediate",
        "goal": "Automate safe and useful local tasks.",
        "concepts": [
            ("Automation", "Automation uses code to perform repetitive work."),
            ("Pathlib", "pathlib provides tools for filesystem paths."),
            ("Subprocess", "subprocess can run external programs; use it carefully."),
            ("Arguments", "Pass command arguments as a list rather than unsafe shell strings when possible."),
            ("Safety", "Test automation before allowing it to modify important files."),
        ],
        "example": 'from pathlib import Path\n\nfor path in Path(".").iterdir():\n    print(path.name)',
        "exercises": [
            "List files in the current directory.",
            "Find files with a specific extension.",
            "Count files in a directory.",
            "Create a directory.",
            "Create a text report.",
            "Rename a test file safely.",
            "Copy a file.",
            "Use subprocess for a harmless local command.",
            "Add a dry-run option.",
            "Build a file-organizing utility for a test directory.",
        ],
        "challenge": "Build a safe file organizer that operates only inside a chosen test directory.",
        "hints": [
            "Use pathlib.Path.",
            "Test with dummy files first.",
            "A dry-run mode can show what would happen without changing files.",
        ],
    },
    {
        "title": "SQLite",
        "level": "Advanced",
        "goal": "Store structured data locally with SQLite.",
        "concepts": [
            ("Database", "A database stores structured information."),
            ("Table", "A table contains rows and columns."),
            ("Connection", "sqlite3.connect() opens a database connection."),
            ("SQL", "SQL statements create and manipulate database data."),
            ("Parameterized queries", "Use placeholders instead of concatenating user input into SQL."),
            ("Commit", "Changes normally need to be committed when using a file-backed database."),
        ],
        "example": 'import sqlite3\n\ncon = sqlite3.connect(":memory:")\ncon.execute("CREATE TABLE users(name TEXT)")\ncon.execute("INSERT INTO users(name) VALUES (?)", ("Azhar",))\nprint(con.execute("SELECT * FROM users").fetchall())\ncon.close()',
        "exercises": [
            "Create an in-memory SQLite database.",
            "Create a table.",
            "Insert a row.",
            "Insert multiple rows.",
            "Select rows.",
            "Filter rows with WHERE.",
            "Update a row.",
            "Delete a row.",
            "Use a parameterized query.",
            "Build a small SQLite CRUD program.",
        ],
        "challenge": "Build a contact manager backed by SQLite with create, read, update, and delete operations.",
        "hints": [
            "Use sqlite3.connect().",
            "Use ? placeholders for values.",
            "Keep SQL structure separate from user-provided values.",
        ],
    },
    {
        "title": "Async Basics",
        "level": "Advanced",
        "goal": "Understand async, await and asynchronous tasks.",
        "concepts": [
            ("async", "async def defines a coroutine function."),
            ("await", "await pauses a coroutine until an awaitable operation completes."),
            ("asyncio", "asyncio provides Python's standard asynchronous framework."),
            ("Task", "asyncio.create_task() schedules a coroutine."),
            ("Concurrency", "Async code can efficiently manage many waiting operations."),
        ],
        "example": 'import asyncio\n\nasync def main():\n    print("Hello async")\n\nasyncio.run(main())',
        "exercises": [
            "Create an async function.",
            "Run it with asyncio.run().",
            "Use asyncio.sleep().",
            "Create two async functions.",
            "Run tasks concurrently.",
            "Measure a simple async operation.",
            "Use create_task().",
            "Handle an async exception.",
            "Build an async worker example.",
            "Build a small async task runner.",
        ],
        "challenge": "Build an async task runner that schedules several simulated waiting tasks concurrently.",
        "hints": [
            "Import asyncio.",
            "Use async def for coroutines.",
            "Use await asyncio.sleep(...) for a safe demonstration.",
        ],
    },
    {
        "title": "Advanced Python",
        "level": "Advanced",
        "goal": "Explore decorators, generators, context managers and advanced syntax.",
        "concepts": [
            ("Decorator", "A decorator wraps or modifies function behavior."),
            ("Generator", "A generator yields values lazily."),
            ("yield", "yield produces a value and pauses a generator."),
            ("Context manager", "A context manager handles setup and cleanup around a block."),
            ("Type hints", "Type hints document expected types and improve tooling."),
        ],
        "example": 'def log_call(fn):\n    def wrapper(*args, **kwargs):\n        print("Calling function")\n        return fn(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef hello(name):\n    print("Hello", name)\n\nhello("Azhar")',
        "exercises": [
            "Create a simple decorator.",
            "Create a decorator that accepts arguments.",
            "Create a generator with yield.",
            "Iterate over a generator.",
            "Create a context manager with with.",
            "Add type hints to a function.",
            "Use a dataclass.",
            "Create a custom iterator.",
            "Combine a decorator with a function returning a value.",
            "Refactor a small program using one advanced feature.",
        ],
        "challenge": "Build a small reusable utility using a decorator, generator, or context manager and explain why you chose it.",
        "hints": [
            "A decorator receives a function and returns a function.",
            "Generators use yield.",
            "Choose the advanced feature that makes the program clearer.",
        ],
    },
    {
        "title": "Security-Focused Python",
        "level": "Advanced",
        "goal": "Practice safe, defensive and security-aware Python.",
        "concepts": [
            ("Secure randomness", "Use secrets rather than random for security-sensitive tokens."),
            ("Input validation", "Validate input before using it."),
            ("Least privilege", "Programs should request only the permissions they need."),
            ("Secrets", "Do not hard-code API keys or passwords in source code."),
            ("Authorized testing", "Only test systems and data you own or are explicitly authorized to test."),
        ],
        "example": 'import secrets\n\ntoken = secrets.token_hex(16)\nprint(token)',
        "exercises": [
            "Generate a secure token with secrets.",
            "Generate a secure random URL-safe token.",
            "Validate a username format.",
            "Validate numeric input.",
            "Keep a secret out of source code.",
            "Read a non-secret configuration value from an environment variable.",
            "Hash a password using a suitable password-hashing library in an authorized project.",
            "Avoid unsafe string-built SQL.",
            "Create a safe file-name validator.",
            "Write a security checklist for a small Python app.",
        ],
        "challenge": "Build a defensive input-validation utility that rejects unsafe or malformed input and explains why.",
        "hints": [
            "Use secrets for security-sensitive random values.",
            "Never place real API keys in source code.",
            "Keep examples focused on systems and data you are authorized to use.",
        ],
    },
    {
        "title": "Project Challenge",
        "level": "Advanced",
        "goal": "Combine your Python skills in a practical CLI project.",
        "concepts": [
            ("Plan", "Define the problem, inputs, outputs, and features."),
            ("Design", "Break the project into functions, modules, or classes."),
            ("Build", "Implement one small feature at a time."),
            ("Test", "Test normal inputs, invalid inputs, and edge cases."),
            ("Document", "Explain how another user can install and run the project."),
        ],
        "example": 'print("Build something useful!")',
        "exercises": [
            "Write a project idea.",
            "Define three requirements.",
            "Design the menu.",
            "Define the data model.",
            "Create the first function.",
            "Create input validation.",
            "Add persistent storage if needed.",
            "Add error handling.",
            "Add tests.",
            "Write a README section for your project.",
        ],
        "challenge": "Build a complete command-line application using multiple Python concepts you have learned.",
        "hints": [
            "Start small.",
            "Separate input, logic, and output.",
            "Test each feature before adding the next.",
        ],
    },
    {
        "title": "Final Project",
        "level": "Advanced",
        "goal": "Plan, build, test and document a complete Python application.",
        "concepts": [
            ("Requirements", "Write down exactly what the application must do."),
            ("Architecture", "Split the application into understandable components."),
            ("Implementation", "Build features incrementally."),
            ("Testing", "Verify normal behavior, edge cases, and failures."),
            ("Security", "Protect secrets and validate untrusted input."),
            ("Documentation", "Make installation and usage clear."),
        ],
        "example": 'print("Your Python journey starts here!")',
        "exercises": [
            "Choose a final project idea.",
            "Write the project requirements.",
            "Create the project structure.",
            "Implement the core feature.",
            "Add input validation.",
            "Add error handling.",
            "Add persistent storage if needed.",
            "Add tests.",
            "Review security and secrets handling.",
            "Document installation and usage.",
        ],
        "challenge": "Build and document your own complete Python project. Use the skills from the entire roadmap.",
        "hints": [
            "Choose a project that is useful and achievable.",
            "Build in small tested steps.",
            "Do not put real credentials in your source code.",
        ],
    },
]


# ============================================================
# GLOBAL API KEY
# ============================================================

API_KEY = ""


# ============================================================
# BASIC UI
# ============================================================

def clear():
    os.system("clear")


def pause(message="Press ENTER to continue..."):
    try:
        input(f"\n{CYAN}{message}{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass


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
    print(f"{MAGENTA}{BOLD}       by Azhar • HCO Team{RESET}")
    print()


def header(title):
    clear()
    logo()
    print(f"{CYAN}{BOLD}{title}{RESET}")
    print("=" * 58)
    print()


# ============================================================
# STARTUP
# ============================================================

def open_youtube():
    commands = [
        ["termux-open-url", YOUTUBE_URL],
        ["am", "start", "-a", "android.intent.action.VIEW", YOUTUBE_URL],
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


def startup():
    clear()

    print(f"{RED}{BOLD}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                 🐍 HCO PYTHONTUTOR 🐍                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")

    print(
        f"{YELLOW}{BOLD}"
        "Since you are learning Python for FREE using Hackers Colony's Free Tool,"
        f"{RESET}"
    )
    print(
        f"{WHITE}"
        "it's a request to please subscribe and click on the Bell 🔔 icon "
        "to support us."
        f"{RESET}\n"
    )

    print(f"{CYAN}{BOLD}📺 Hackers Colony Tech{RESET}")
    print(f"{CYAN}{YOUTUBE_URL}{RESET}\n")

    print(
        f"{GREEN}{BOLD}"
        "Now Termux will redirect you to YouTube App in:"
        f"{RESET}\n"
    )

    for number in range(9, 0, -1):
        print(f"{YELLOW}{BOLD}                         {number}{RESET}")
        time.sleep(1)

    print(f"\n{GREEN}{BOLD}📱 Opening Hackers Colony Tech...{RESET}")
    time.sleep(0.7)

    if not open_youtube():
        print(f"{RED}⚠️ Could not open YouTube automatically.{RESET}")
        print(f"{CYAN}{YOUTUBE_URL}{RESET}")

    print()
    pause("↩️ Come back here and press ENTER to continue...")


# ============================================================
# PROGRESS
# ============================================================

def default_progress():
    return {
        "current_lesson": 1,
        "current_exercise": 1,
        "completed_lessons": [],
        "lesson_exercises": {},
        "completed_challenges": 0,
        "daily_sessions": 0,
        "xp": 0,
        "streak": 0,
        "last_day": "",
    }


def load_progress():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    default = default_progress()

    if not PROGRESS_FILE.exists():
        return default

    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            default.update(data)
        return default
    except Exception:
        return default


def save_progress(progress):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(
        json.dumps(progress, indent=2),
        encoding="utf-8",
    )


def lesson_completed(progress, number):
    return number in progress.get("completed_lessons", [])


def exercise_count(progress, number):
    values = progress.get("lesson_exercises", {}).get(str(number), [])
    return len(values)


def mark_exercise_complete(progress, lesson_number, exercise_number):
    lesson_data = progress.setdefault("lesson_exercises", {})
    done = lesson_data.setdefault(str(lesson_number), [])

    if exercise_number not in done:
        done.append(exercise_number)
        done.sort()
        progress["xp"] = progress.get("xp", 0) + 5

    save_progress(progress)


def mark_lesson_complete(progress, number):
    completed = progress.setdefault("completed_lessons", [])

    if number not in completed:
        completed.append(number)
        completed.sort()
        progress["xp"] = progress.get("xp", 0) + 25

    if number < len(LESSONS):
        progress["current_lesson"] = number + 1
        progress["current_exercise"] = 1
    else:
        progress["current_lesson"] = len(LESSONS)
        progress["current_exercise"] = len(LESSONS[number - 1]["exercises"])

    save_progress(progress)


def update_streak(progress):
    today = date.today()
    last = progress.get("last_day", "")

    if last == str(today):
        return

    if last:
        try:
            previous = date.fromisoformat(last)
            if today == previous + timedelta(days=1):
                progress["streak"] = progress.get("streak", 0) + 1
            else:
                progress["streak"] = 1
        except ValueError:
            progress["streak"] = 1
    else:
        progress["streak"] = 1

    progress["last_day"] = str(today)


def progress_bar(progress):
    total = len(LESSONS)
    completed = len(progress.get("completed_lessons", []))
    width = 28
    filled = int(width * completed / total)

    return (
        f"{GREEN}{'█' * filled}"
        f"{BLUE}{'░' * (width - filled)}"
        f"{RESET} {completed}/{total}"
    )


# ============================================================
# CODE EXECUTION
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
            return output if output else "✅ Code ran successfully with no output."

        return (output + "\n" if output else "") + errors

    except subprocess.TimeoutExpired:
        return f"⏱️ Execution stopped after {timeout} seconds."
    except Exception as error:
        return f"Execution error: {error}"


def multiline_input():
    print(f"{YELLOW}{BOLD}Code input rules:{RESET}")
    print("• Type only Python code.")
    print("• Do NOT type >>> or ...")
    print("• Type END alone on a new line when finished.")
    print()

    lines = []

    while True:
        try:
            prompt = ">>> " if not lines else "... "
            line = input(prompt)
        except (KeyboardInterrupt, EOFError):
            return ""

        if line.strip() == "END":
            return "\n".join(lines)

        lines.append(line)


# ============================================================
# SIMPLE TASK CHECKING
# ============================================================

def check_task(lesson_number, exercise_number, code):
    """
    Lightweight checks for early lessons.
    Later lessons primarily verify that code runs successfully.
    This intentionally does not claim to be a full test framework.
    """
    normalized = code.replace(" ", "").replace("\t", "")

    if lesson_number == 1:
        if exercise_number == 1:
            return "print(" in normalized and "Hello" in code
        if exercise_number == 2:
            return "print(" in normalized
        if exercise_number == 3:
            return "print(" in normalized and "learningPython" in normalized
        if exercise_number == 4:
            return normalized.count("print(") >= 2
        if exercise_number == 5:
            return "print(" in normalized
        return "print(" in normalized

    if lesson_number == 2:
        if exercise_number <= 2:
            return "=" in code and "print(" in normalized
        return "=" in code

    if lesson_number == 3:
        if exercise_number <= 5:
            return "type(" in normalized or "print(" in normalized
        return True

    if lesson_number == 4:
        return "input(" in normalized

    if lesson_number == 5:
        return any(op in code for op in ["+", "-", "*", "/", "%"])

    if lesson_number == 6:
        return "if" in code

    if lesson_number in (7, 8):
        return "for" in code if lesson_number == 7 else "while" in code

    if lesson_number == 9:
        return "[" in code and "]" in code

    if lesson_number == 10:
        return "{" in code or "set(" in normalized or "(" in code

    if lesson_number == 11:
        return "{" in code and ":" in code

    if lesson_number == 12:
        return "def" in code

    return True


# ============================================================
# LEARN MODE
# ============================================================

def show_lesson_overview(number, lesson):
    header(f"📚 LESSON {number:02d} — {lesson['title']}")

    print(f"{YELLOW}{BOLD}Level:{RESET} {lesson['level']}")
    print(f"{YELLOW}{BOLD}Goal:{RESET} {lesson['goal']}\n")

    print(f"{MAGENTA}{BOLD}What you will learn:{RESET}")

    for index, (name, explanation) in enumerate(
        lesson["concepts"], 1
    ):
        print(f"{CYAN}{index}.{RESET} {name}")
        print(f"   {explanation}")

    print()
    print(f"{YELLOW}{BOLD}Example:{RESET}")
    print(f"{GREEN}{lesson['example']}{RESET}")

    print()
    print(f"{BLUE}{BOLD}Example output:{RESET}")
    print(run_python(lesson["example"]))

    pause()


def guided_exercise(progress, lesson_number, exercise_number):
    lesson = LESSONS[lesson_number - 1]
    task = lesson["exercises"][exercise_number - 1]

    header(
        f"🧪 LESSON {lesson_number:02d} "
        f"• EXERCISE {exercise_number:02d}/10"
    )

    print(f"{CYAN}{BOLD}{lesson['title']}{RESET}\n")
    print(f"{YELLOW}{BOLD}Task:{RESET}")
    print(task)

    print()
    print(f"{BLUE}Before coding:{RESET}")
    print("Think about which concept from this lesson you need.")
    print("The tool will run your code locally and show the result.")

    print()
    print(f"{MAGENTA}Hints are available from the menu below after an attempt.{RESET}")
    print()

    code = multiline_input()

    if not code.strip():
        return False

    output = run_python(code)

    print(f"\n{YELLOW}{BOLD}▶ Output:{RESET}")
    print(output)

    syntax_error = "SyntaxError:" in output
    runtime_error = "Traceback" in output or "Error:" in output

    if syntax_error or runtime_error:
        print(f"\n{RED}{BOLD}❌ The code needs fixing.{RESET}")
        print("Read the error and try again.")
        print("You can use the AI Tutor for guided help.")
        pause()
        return False

    if check_task(lesson_number, exercise_number, code):
        mark_exercise_complete(
            progress,
            lesson_number,
            exercise_number,
        )

        print(f"\n{GREEN}{BOLD}✅ Exercise completed! +5 XP{RESET}")
        pause()
        return True

    print(
        f"\n{YELLOW}{BOLD}"
        "⚠️ Your code ran, but it may not satisfy the task yet."
        f"{RESET}"
    )

    print("Use a hint or try again.")
    pause()
    return False


def learn_step_by_step(progress):
    while True:
        number = min(
            max(progress.get("current_lesson", 1), 1),
            len(LESSONS),
        )

        lesson = LESSONS[number - 1]
        show_lesson_overview(number, lesson)

        completed = set(
            progress.get("lesson_exercises", {})
            .get(str(number), [])
        )

        while len(completed) < 10:
            next_exercise = next(
                (
                    i for i in range(1, 11)
                    if i not in completed
                ),
                1,
            )

            success = guided_exercise(
                progress,
                number,
                next_exercise,
            )

            completed = set(
                progress.get("lesson_exercises", {})
                .get(str(number), [])
            )

            if not success:
                while True:
                    header(
                        f"📚 LESSON {number:02d} "
                        f"• PRACTICE {len(completed)}/10"
                    )

                    print(f"[1] 🔁 Retry Exercise {next_exercise}")
                    print("[2] 💡 Show Hint")
                    print("[3] 🤖 Ask AI Tutor")
                    print("[4] 📖 Review Lesson")
                    print("[0] ↩️ Return to Main Menu")
                    print()

                    try:
                        choice = input(
                            f"{MAGENTA}Lesson Practice > {RESET}"
                        ).strip()
                    except (KeyboardInterrupt, EOFError):
                        return

                    if choice == "1":
                        break

                    if choice == "2":
                        hints = lesson["hints"]
                        print()
                        for i, hint in enumerate(hints, 1):
                            print(f"{YELLOW}{i}. {hint}{RESET}")
                        pause()

                    elif choice == "3":
                        ai_tutor(
                            API_KEY,
                            progress,
                            context=(
                                f"The student is on lesson {number}, "
                                f"exercise {next_exercise}. "
                                f"Task: {lesson['exercises'][next_exercise - 1]}"
                            ),
                        )

                    elif choice == "4":
                        show_lesson_overview(number, lesson)

                    elif choice == "0":
                        return

                continue

        mark_lesson_complete(progress, number)

        header(f"🎉 LESSON {number:02d} COMPLETE")
        print(
            f"{GREEN}{BOLD}"
            "You completed all 10 guided exercises!"
            f"{RESET}"
        )
        print(f"XP: {progress.get('xp', 0)}")

        if number < len(LESSONS):
            print()
            print(
                f"{CYAN}"
                f"Next lesson: {LESSONS[number]['title']}"
                f"{RESET}"
            )

        pause()

        if number >= len(LESSONS):
            return


# ============================================================
# DAILY 10-MINUTE MODE
# ============================================================

def daily_10_minutes(progress):
    number = min(
        max(progress.get("current_lesson", 1), 1),
        len(LESSONS),
    )
    lesson = LESSONS[number - 1]

    header("🕐 DAILY 10-MINUTE LEARNING")

    print(
        f"{CYAN}{BOLD}"
        f"Today's lesson: {number:02d} — {lesson['title']}"
        f"{RESET}\n"
    )

    print(f"{YELLOW}{BOLD}1. Learn{RESET}")
    print(lesson["goal"])

    for name, explanation in lesson["concepts"][:3]:
        print(f"\n{CYAN}{name}:{RESET} {explanation}")

    print(f"\n{YELLOW}{BOLD}2. Example{RESET}")
    print(f"{GREEN}{lesson['example']}{RESET}")
    print("Output:")
    print(run_python(lesson["example"]))

    print()
    print(f"{YELLOW}{BOLD}3. Practice{RESET}")
    exercise_number = min(
        max(progress.get("current_exercise", 1), 1),
        10,
    )
    print(
        f"Today's exercise {exercise_number}/10:"
    )
    print(
        lesson["exercises"][exercise_number - 1]
    )

    print()
    code = multiline_input()

    if not code.strip():
        return

    output = run_python(code)

    print(f"\n{YELLOW}{BOLD}▶ Output:{RESET}")
    print(output)

    if (
        "SyntaxError:" in output
        or "Traceback" in output
        or "Error:" in output
    ):
        print(f"\n{RED}Fix the problem and try again tomorrow or retry now.{RESET}")
        pause()
        return

    if not check_task(number, exercise_number, code):
        print(
            f"\n{YELLOW}"
            "The code ran, but the exercise may not be complete yet."
            f"{RESET}"
        )
        pause()
        return

    mark_exercise_complete(
        progress,
        number,
        exercise_number,
    )

    progress["daily_sessions"] = (
        progress.get("daily_sessions", 0) + 1
    )
    progress["xp"] = progress.get("xp", 0) + 10
    update_streak(progress)

    if exercise_number < 10:
        progress["current_exercise"] = exercise_number + 1
    else:
        mark_lesson_complete(progress, number)
        progress["current_exercise"] = 1

    save_progress(progress)

    print(
        f"\n{GREEN}{BOLD}"
        "🎉 Daily session complete! +10 XP"
        f"{RESET}"
    )
    print(
        f"🔥 Streak: {progress.get('streak', 0)} day(s)"
    )
    print(
        "Come back tomorrow for another focused session."
    )

    pause()


# ============================================================
# PRACTICE LAB
# ============================================================

def practice_lab():
    while True:
        header("🧪 PRACTICE LAB")

        print("A free Python playground.")
        print("There is no lesson requirement and no challenge scoring.")
        print()

        print("[1] ▶ Run Python Code")
        print("[2] 📖 Quick Syntax Reference")
        print("[3] 🧹 Clear Screen")
        print("[0] ↩️ Return")
        print()

        try:
            choice = input(
                f"{MAGENTA}Practice Lab > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == "1":
            print()
            code = multiline_input()
            if code.strip():
                print(f"\n{YELLOW}▶ Output:{RESET}")
                print(run_python(code))
                pause()

        elif choice == "2":
            header("📖 PYTHON QUICK REFERENCE")
            print('print("Hello")       → display text')
            print('name = "Azhar"      → create a variable')
            print('input("Name: ")      → get user input')
            print("if x > 5:           → condition")
            print("for i in range(5):  → loop")
            print("while x < 5:        → while loop")
            print("[1, 2, 3]           → list")
            print('{"name": "Azhar"}    → dictionary')
            print("def greet():        → function")
            pause()

        elif choice == "3":
            clear()

        elif choice == "0":
            return


# ============================================================
# CHALLENGE MODE
# ============================================================

def challenge_mode(progress):
    number = min(
        max(progress.get("current_lesson", 1), 1),
        len(LESSONS),
    )

    lesson = LESSONS[number - 1]

    while True:
        header("🎯 CODING CHALLENGE")

        print(f"{CYAN}{BOLD}Current level: {lesson['level']}{RESET}")
        print(f"Topic: {lesson['title']}\n")

        print("[1] 🟢 Warm-up")
        print("[2] 🟡 Medium")
        print("[3] 🔴 Hard")
        print("[4] 👑 Boss Challenge")
        print("[0] ↩️ Return")
        print()

        try:
            choice = input(
                f"{MAGENTA}Challenge > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == "0":
            return

        challenge = lesson["challenge"]

        if choice == "1":
            task = lesson["exercises"][0]
            difficulty = "Warm-up"

        elif choice == "2":
            task = lesson["exercises"][4]
            difficulty = "Medium"

        elif choice == "3":
            task = lesson["exercises"][8]
            difficulty = "Hard"

        elif choice == "4":
            task = challenge
            difficulty = "Boss Challenge"

        else:
            continue

        header(f"🎯 {difficulty.upper()} CHALLENGE")

        print(f"{YELLOW}{BOLD}Task:{RESET}")
        print(task)

        print()
        print(
            "You may use the concepts from your current and previous lessons."
        )
        print("Type END alone on a new line when finished.\n")

        code = multiline_input()

        if not code.strip():
            continue

        output = run_python(code)

        print(f"\n{YELLOW}{BOLD}▶ Output:{RESET}")
        print(output)

        if (
            "SyntaxError:" in output
            or "Traceback" in output
            or "Error:" in output
        ):
            print(f"\n{RED}{BOLD}❌ Challenge failed. Fix the code and retry.{RESET}")
            pause()
            continue

        progress["completed_challenges"] = (
            progress.get("completed_challenges", 0) + 1
        )

        progress["xp"] = progress.get("xp", 0) + 20

        save_progress(progress)

        print(
            f"\n{GREEN}{BOLD}"
            "🎉 Challenge submitted successfully! +20 XP"
            f"{RESET}"
        )

        pause()
        return


# ============================================================
# AI TUTOR
# ============================================================

SYSTEM_PROMPT = """You are HCO PythonTutor, an interactive Python teacher for
Termux and Linux.

The student may be an absolute beginner.

Teach instead of simply dumping answers.

When teaching a concept:
1. Explain it in simple English.
2. Explain important syntax and symbols.
3. Show a small example.
4. Ask the student a quick check question.
5. Give a small practice task.
6. Prefer hints before complete solutions.
7. If code has an error, identify the error and explain the next step.
8. Do not pretend that you executed code. The local HCO PythonTutor executes it.
9. Keep responses practical and suitable for terminal-based learning.

For cybersecurity examples, remain legal, authorized, defensive, and educational.
Do not provide instructions for unauthorized access, malware, credential theft,
or attacks against real systems."""


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
            f"API error ({response.status_code}): "
            f"{data.get('error', data)}"
        )

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response format from OpenRouter.")


def ai_tutor(api_key, progress, context=""):
    while True:
        header("🤖 HCO AI TUTOR")

        current = min(
            max(progress.get("current_lesson", 1), 1),
            len(LESSONS),
        )
        lesson = LESSONS[current - 1]

        print(
            f"{CYAN}{BOLD}"
            f"Current lesson: {current:02d} — {lesson['title']}"
            f"{RESET}"
        )

        print()
        print("[1] 📖 Learn a Concept")
        print("[2] 🧠 Interactive Quiz")
        print("[3] 🐛 Debug My Code")
        print("[4] 💡 Get a Hint")
        print("[5] 🗺️ Explain My Learning Path")
        print("[6] 💬 Ask a Python Question")
        print("[0] ↩️ Return")
        print()

        try:
            choice = input(
                f"{MAGENTA}AI Tutor > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == "0":
            return

        if choice == "1":
            prompt = (
                f"Teach me the concept '{lesson['title']}' from absolute beginner level. "
                "Explain the syntax and symbols, show one tiny example, then ask me "
                "one short question to check understanding. Do not give a long unrelated lecture."
            )

        elif choice == "2":
            prompt = (
                f"Create a short interactive Python quiz about '{lesson['title']}'. "
                "Ask ONE question only and wait for my answer. Do not reveal the answer immediately."
            )

        elif choice == "3":
            header("🐛 AI DEBUGGER")
            print("Paste the code that is causing trouble.")
            print()
            code = multiline_input()

            if not code.strip():
                continue

            prompt = (
                f"The student is learning '{lesson['title']}'.\n"
                "Analyze this Python code as a teacher. Explain the error or problem, "
                "give one small next step, and ask the student to try fixing it.\n\n"
                f"Code:\n{code}"
            )

        elif choice == "4":
            exercise_number = min(
                max(progress.get("current_exercise", 1), 1),
                10,
            )
            task = lesson["exercises"][exercise_number - 1]

            prompt = (
                f"The student is working on this exercise:\n{task}\n\n"
                "Give ONE helpful hint without giving the complete solution."
            )

        elif choice == "5":
            completed = len(progress.get("completed_lessons", []))
            prompt = (
                f"Explain the student's current Python learning path. "
                f"They have completed {completed} of {len(LESSONS)} lessons and "
                f"are currently on '{lesson['title']}'. "
                "Explain what they have learned, what they are learning now, "
                "and what the next few concepts will build on."
            )

        elif choice == "6":
            try:
                question = input(
                    f"{CYAN}Your Python question > {RESET}"
                ).strip()
            except (KeyboardInterrupt, EOFError):
                continue

            if not question:
                continue

            prompt = (
                f"The student is currently learning '{lesson['title']}'.\n"
                f"Student question: {question}\n\n"
                "Teach the answer clearly. If it is a new concept, explain it from basics."
            )

        else:
            continue

        if context:
            prompt = context + "\n\n" + prompt

        print(f"\n{YELLOW}⏳ AI Tutor is thinking...{RESET}\n")

        try:
            answer = ask_ai(api_key, prompt)
            print(f"{GREEN}{BOLD}🤖 HCO AI TUTOR{RESET}\n")
            print(answer)
        except Exception as error:
            print(f"{RED}❌ {error}{RESET}")

        pause()


# ============================================================
# PROGRESS SCREEN
# ============================================================

def show_progress(progress):
    header("📊 MY PYTHON PROGRESS")

    print(f"Overall: {progress_bar(progress)}")
    print(f"⭐ XP: {progress.get('xp', 0)}")
    print(f"🔥 Streak: {progress.get('streak', 0)} day(s)")
    print(
        f"🎯 Challenges completed: "
        f"{progress.get('completed_challenges', 0)}"
    )
    print(
        f"🕐 Daily sessions: "
        f"{progress.get('daily_sessions', 0)}"
    )
    print()

    current = progress.get("current_lesson", 1)
    current_exercise = progress.get("current_exercise", 1)

    print(
        f"{CYAN}{BOLD}"
        f"Current lesson: {current:02d} — "
        f"{LESSONS[current - 1]['title']}"
        f"{RESET}"
    )

    print(
        f"Current exercise: "
        f"{current_exercise}/10"
    )

    print()
    print(f"{YELLOW}{BOLD}Lesson Progress:{RESET}")

    for index, lesson in enumerate(LESSONS, 1):
        exercises = exercise_count(progress, index)
        done = lesson_completed(progress, index)

        mark = (
            f"{GREEN}✓{RESET}"
            if done
            else f"{BLUE}○{RESET}"
        )

        print(
            f"{mark} {index:02d}. "
            f"{lesson['title']} "
            f"[{exercises}/10]"
        )

    pause()


# ============================================================
# SETTINGS
# ============================================================

def settings_menu():
    while True:
        header("⚙️ SETTINGS")

        print("[1] 🔐 Change OpenRouter API Key")
        print("[2] 🗂️ Show Progress File Location")
        print("[3] ⚠️ Reset Learning Progress")
        print("[0] ↩️ Return")
        print()

        try:
            choice = input(
                f"{MAGENTA}Settings > {RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == "1":
            global API_KEY
            API_KEY = get_api_key()
            print(f"{GREEN}API key updated for this session.{RESET}")
            pause()

        elif choice == "2":
            print(f"\nProgress file:")
            print(PROGRESS_FILE)
            pause()

        elif choice == "3":
            confirm = input(
                "Type RESET to delete your learning progress: "
            ).strip()

            if confirm == "RESET":
                try:
                    if PROGRESS_FILE.exists():
                        PROGRESS_FILE.unlink()
                    print(
                        f"{GREEN}"
                        "Progress reset. Restart the tool to reload defaults."
                        f"{RESET}"
                    )
                except Exception as error:
                    print(f"{RED}Could not reset: {error}{RESET}")
            else:
                print("Reset cancelled.")

            pause()

        elif choice == "0":
            return


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
        "for AI Tutor features."
    )
    print(
        "The key is entered locally and is not stored in the source code."
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
        print(f"Progress: {progress_bar(progress)}")
        print(
            f"⭐ XP: {progress.get('xp', 0)}   "
            f"🔥 Streak: {progress.get('streak', 0)}"
        )
        print()

        print(f"{CYAN}[1]{RESET} 📚 Learn Step-by-Step")
        print(f"{GREEN}[2]{RESET} 🕐 Daily 10-Minute Learning")
        print(f"{MAGENTA}[3]{RESET} 🧪 Practice Lab")
        print(f"{BLUE}[4]{RESET} 🎯 Coding Challenge")
        print(f"{YELLOW}[5]{RESET} 🤖 AI Tutor")
        print(f"{CYAN}[6]{RESET} 📊 My Progress")
        print(f"{WHITE}[7]{RESET} ⚙️ Settings")
        print(f"{RED}[0]{RESET} 🚪 Exit")
        print()

        try:
            choice = input(
                f"{MAGENTA}{BOLD}"
                "HCO PythonTutor > "
                f"{RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! 👋")
            return

        if choice == "1":
            learn_step_by_step(progress)

        elif choice == "2":
            daily_10_minutes(progress)

        elif choice == "3":
            practice_lab()

        elif choice == "4":
            challenge_mode(progress)

        elif choice == "5":
            ai_tutor(API_KEY, progress)

        elif choice == "6":
            show_progress(progress)

        elif choice == "7":
            settings_menu()

        elif choice == "0":
            print(
                f"\n{GREEN}"
                "Keep learning. Keep building. 🐍🔥"
                f"{RESET}"
            )
            return

        else:
            pause("❌ Invalid option. Press ENTER...")


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
        "Learn → Understand → Practice → Run → Fix → Challenge → Progress"
    )

    time.sleep(2)

    main_menu(progress)


if __name__ == "__main__":
    main()
