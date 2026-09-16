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
        "task": "Create a virt
