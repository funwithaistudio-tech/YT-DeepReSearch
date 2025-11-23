#!/bin/bash

# YT-DeepReSearch Setup Script
# This script sets up the YT-DeepReSearch environment

set -e

echo "=================================="
echo "YT-DeepReSearch Setup"
echo "=================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10 or higher required. Found: $python_version"
    exit 1
fi
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p input output logs
touch input/.gitkeep output/.gitkeep logs/.gitkeep
echo "✓ Directories created"

# Setup environment file
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys:"
    echo "   - PERPLEXITY_API_KEY"
    echo "   - GEMINI_API_KEY"
    echo "   - GOOGLE_CLOUD_PROJECT"
else
    echo "✓ .env file already exists"
fi

# Create sample Excel file
echo ""
echo "Creating sample Excel queue..."
python3 << EOF
import sys
sys.path.insert(0, 'src')
from orchestrator.excel_queue_manager import ExcelQueueManager
manager = ExcelQueueManager('./input/topics.xlsx')
print('✓ Sample Excel queue created at ./input/topics.xlsx')
EOF

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v -q
echo "✓ Tests passed"

echo ""
echo "=================================="
echo "Setup complete! 🎉"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Add topics to ./input/topics.xlsx"
echo "3. Run: python src/main.py --mode queue"
echo ""
echo "For help: python src/main.py --help"
echo "=================================="
