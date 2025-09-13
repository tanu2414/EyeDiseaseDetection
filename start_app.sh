#!/bin/bash

# Eye Disease Prediction Application Startup Script
# This script initializes and starts the Flask application

echo "🚀 Starting Eye Disease Prediction Application"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir -p uploads
    echo "✅ Uploads directory created"
fi

# Create instance directory if it doesn't exist
if [ ! -d "instance" ]; then
    echo "📁 Creating instance directory..."
    mkdir -p instance
    echo "✅ Instance directory created"
fi

# Check if database exists, if not initialize it
if [ ! -f "instance/database.db" ]; then
    echo "🗄️  Initializing database..."
    python3 -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
"
fi

# Check if model file exists
if [ ! -f "models/MultipleEyeDiseaseDetectModel.pth" ]; then
    echo "⚠️  Warning: ML model file not found at models/MultipleEyeDiseaseDetectModel.pth"
    echo "   The application may not work properly without the trained model."
    echo "   Please ensure the model file is in the correct location."
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "⚠️  Warning: Some dependencies may not have installed correctly"
    fi
fi

echo ""
echo "🌟 Starting Flask Application..."
echo "📍 Application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 run.py