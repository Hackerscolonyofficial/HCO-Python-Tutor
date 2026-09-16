# 🐍 HCO PythonTutor

### AI-Powered Python Learning Companion for Termux & Linux

**Code by Azhar (A-Z-H-A-R) • HCO Team**

> “The quieter you become, the more you are able to hear.”

HCO PythonTutor is an interactive terminal-based learning tool designed to help you learn Python from **Beginner → Advanced** with lessons, hands-on practice, real local Python execution, coding challenges, progress tracking, and an optional AI tutor.

## 🚀 Learning Philosophy

This is not only a text reader or chatbot.

**Learn → Write → Run → Check → Fix → Challenge → Progress**

You can write and execute Python directly inside the terminal.

## ✨ Features

- 🐍 30-step Beginner → Advanced roadmap
- 📚 Step-by-step lessons
- 🕐 Daily 10-minute learning mode
- 🧪 Practice Lab inside Termux/Linux
- ▶️ Run your own Python code locally
- 🎯 Coding challenges
- 🤖 AI Python Tutor via OpenRouter
- 📊 Local progress tracking
- 🎨 Colorful terminal interface
- 📱 Termux + Linux support
- 🔐 Bring your own OpenRouter API key

## 📱 Termux Installation

### 1. Install Git

```bash
pkg update -y
pkg install -y git
```

### 2. Clone the repository

```bash
git clone https://github.com/Hackerscolonyofficial/HCO-PythonTutor.git
```

### 3. Enter the folder

```bash
cd HCO-PythonTutor
```

### 4. Install and launch

```bash
bash install.sh
```

The installer installs Python and the required dependency, then launches HCO PythonTutor automatically.

## 🐧 Linux Installation

### 1. Install Git

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y git
```

### 2. Clone

```bash
git clone https://github.com/Hackerscolonyofficial/HCO-PythonTutor.git
```

### 3. Enter the folder

```bash
cd HCO-PythonTutor
```

### 4. Install and launch

```bash
bash install.sh
```

The installer can automatically install Python 3 and pip on Debian/Ubuntu-style systems.

For other Linux distributions, install Python 3 and pip with your distribution's package manager, then run:

```bash
bash install.sh
```

## 🤖 OpenRouter API Key

HCO PythonTutor uses your own OpenRouter API key for the AI Tutor.

The key is entered locally using a hidden password prompt and is not included in the GitHub source.

The practical learning and local Python execution features do not depend on the AI API. The key is required for **Ask AI Tutor**.

### Security

- Never publish your API key.
- Never commit a real key to GitHub.
- If a key is exposed, revoke/rotate it with your provider.
- `.gitignore` is included to help avoid accidental secret commits.

## 🧠 Curriculum

### Beginner

1. Python & print()
2. Variables
3. Data Types
4. Input
5. Operators
6. Conditions
7. for Loops
8. while Loops
9. Lists
10. Tuples & Sets
11. Dictionaries
12. Functions

### Intermediate

13. Function Arguments & Scope
14. Modules
15. File Handling
16. Exceptions
17. Comprehensions
18. OOP Basics
19. Inheritance
20. Virtual Environments
21. JSON & APIs
22. Testing

### Advanced

23. Debugging
24. Automation
25. SQLite
26. Async Basics
27. Advanced Python
28. Security-Focused Python
29. Project Challenge
30. Final Project

## 🧪 Practical Learning

Example:

```text
🐍 LESSON 02 — Variables

🎯 PRACTICE TASK
Create a variable called city and print it.

>>> city = "Jaipur"
>>> print(city)
>>> END

▶ Output:
Jaipur

✅ Code executed successfully!
```

The code is executed locally using the Python interpreter on the user's machine.

## 🕐 Daily 10-Minute Mode

Choose:

```text
[2] 🕐 Daily 10-Minute Learning
```

Each session focuses on the current lesson:

**Learn → Example → Practice → Run → Progress**

The goal is consistent daily learning instead of trying to consume the whole course at once.

## 🎯 Coding Challenges

The challenge mode asks you to solve a task yourself.

The goal is:

**Don't just read Python. Write Python.**

## 🤖 AI Tutor

Ask the AI Tutor about:

- Python concepts
- Syntax
- Errors
- Debugging
- Projects
- Learning strategy
- Code explanations

The AI tutor is instructed to teach with hints and explanations rather than simply dumping solutions.

## 📊 Progress

Progress is saved locally at:

```text
~/.hco_pythontutor/progress.json
```

The tool tracks:

- Completed lessons
- Current lesson
- Coding challenges
- Daily sessions

No external progress database is required.

## 📁 Project Structure

```text
HCO-PythonTutor/
├── HCO-PythonTutor.py
├── install.sh
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## 📺 Hackers Colony Tech

YouTube:

https://youtube.com/@hackers_colony_tech

Community:

https://hcogroup.netlify.app/

## 🛡️ Disclaimer

HCO PythonTutor is provided for informational and educational purposes.

Cybersecurity-related learning should only be performed on systems, devices, networks, and accounts that you own or have explicit permission to test.

Hackers Colony Tech does not support unauthorized access, data theft, malware distribution, or attacks against systems without permission.

You are responsible for how you use the information, code, and tools provided by this project.

## 📜 License

HCO PythonTutor is released under the **HCO PythonTutor Proprietary License**.

Personal educational use is permitted. Redistribution, republishing as your own project, commercial redistribution, and removal of attribution are not permitted without written permission.

See `LICENSE` for the complete terms.

## 👨‍💻 Creator

**Code by Azhar (A-Z-H-A-R) • HCO Team**

### Hackers Colony Tech ⚡

**Learn • Build • Explore • Stay Ethical**

## ⭐ Support HCO

If HCO PythonTutor helps you learn Python:

👍 Star the repository  
📺 Subscribe to Hackers Colony Tech  
🔔 Turn on notifications  
💬 Share your feedback

**Keep learning. Keep building. 🐍🔥**
