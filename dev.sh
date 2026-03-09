#!/usr/bin/env bash

set -e

echo "🔧 Setting up ShellForge development environment..."

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Updating pip..."
pip install --upgrade pip

# Install project in editable mode
echo "📦 Installing ShellForge in editable mode..."
pip install -e .

echo ""
echo "✅ Dev environment ready."
echo ""
echo "Run commands like:"
echo "shellforge --help"
echo "shellforge bootstrap --dry-run"
echo ""