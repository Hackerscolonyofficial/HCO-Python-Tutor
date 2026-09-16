#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
MAGENTA='\033[1;35m'
RESET='\033[0m'
BOLD='\033[1m'

clear

echo -e "${CYAN}${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    HCO PYTHONTUTOR                      ║"
echo "║              INSTALLATION & LAUNCHER                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${RESET}"
echo

if command -v pkg >/dev/null 2>&1; then
    echo -e "${GREEN}📱 Termux detected${RESET}"
    echo -e "${YELLOW}📦 Installing Python...${RESET}"
    pkg update -y
    pkg install -y python
else
    echo -e "${GREEN}🐧 Linux detected${RESET}"

    if command -v python3 >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Python 3 already installed${RESET}"
    elif command -v apt-get >/dev/null 2>&1; then
        if [ "$(id -u)" -eq 0 ]; then
            apt-get update
            apt-get install -y python3 python3-pip
        elif command -v sudo >/dev/null 2>&1; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip
        else
            echo -e "${RED}❌ sudo is required to install Python 3.${RESET}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Could not automatically install Python 3.${RESET}"
        echo "Please install Python 3 and pip manually, then run this script again."
        exit 1
    fi
fi

echo
echo -e "${YELLOW}${BOLD}📦 Installing Python dependencies...${RESET}"
python3 -m pip install -r "$PROJECT_DIR/requirements.txt"

chmod +x "$PROJECT_DIR/HCO-PythonTutor.py"

echo
echo -e "${GREEN}${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✅ INSTALLATION COMPLETE                    ║"
echo "║              🚀 STARTING PYTHON TUTOR                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

sleep 2
exec python3 "$PROJECT_DIR/HCO-PythonTutor.py"
