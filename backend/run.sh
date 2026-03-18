#!/bin/bash
# Quick start script for Skill Track backend

echo "🚀 Starting Skill Track Backend..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install deps
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "   ✏️  Please edit .env with your MySQL credentials, then re-run."
    exit 1
fi

echo "✅ Starting Flask server on http://localhost:5000"
python app.py
