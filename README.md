# 🛡️ Tech Astuces CLI

> A lightweight, open-source CLI toolkit for security checks and code analysis — right from your terminal.

![Python (https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
![License (https://img.shields.io/badge/License-MIT-green)](LICENSE)
![PRs Welcome (https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

---

## 🚀 Features

| Command       | Description |
|---------------|-------------|
| passcheck   | Evaluate password strength and check against known data breaches (no plain-text transmission) |
| headers     | Scan website security headers (HTTPS, HSTS, CSP, X-Frame-Options, etc.) |
| codestats   | Analyze a codebase: lines per language, TODOs, file counts, and more |
| filecheck   | Monitor a folder for file changes: additions, modifications, or deletions |

---

## 📦 Installation

### Prerequisites
- Python 3.7+
- Git
- pip

### Quick Install (Termux / Linux / macOS)

```bash
# Update packages
pkg update && pkg upgrade -y

# Install dependencies
pkg install python git -y

# Clone the repository
git clone https://github.com/Styven-Emmanuel-Dev/TechAstuces-Kit.git
cd TechAstuces-Kit

# Install Python dependencies
pip install -r requirements.txt

# Install the CLI globally
pip install -e .

# Verify installation
techastuces --help
