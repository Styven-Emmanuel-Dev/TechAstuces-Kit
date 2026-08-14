#!/bin/bash
# install.sh — TechAstuces Kit installer
# Run on Termux or any Linux system:
#   curl -sL https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/techastuces-kit/main/install.sh | bash

set -e

echo "⚡ Installing TechAstuces Kit..."

if command -v pkg &> /dev/null; then
  echo "📱 Termux detected."
  pkg update -y && pkg upgrade -y
  pkg install -y python git
else
  echo "🐧 Linux detected."
  command -v python3 &> /dev/null || { echo "Install Python 3 first."; exit 1; }
fi

pip install --upgrade pip --break-system-packages 2>/dev/null || pip install --upgrade pip

REPO_URL="https://github.com/YOUR-GITHUB-USERNAME/techastuces-kit.git"

if [ -d "techastuces-kit" ]; then
  echo "📂 Folder already exists, pulling latest..."
  cd techastuces-kit && git pull
else
  git clone "$REPO_URL"
  cd techastuces-kit
fi

pip install -e . --break-system-packages 2>/dev/null || pip install -e .

echo ""
echo "✅ Installation complete!"
echo "Run: techastuceskit --help"
