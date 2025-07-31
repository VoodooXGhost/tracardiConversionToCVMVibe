#!/bin/bash

# CVM MVP Setup Script for Tmcel
echo "🚀 Setting up CVM MVP for Tmcel..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.9+ is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 18+ is required but not installed."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup database
echo "📊 Setting up database..."
createdb cvm_tmcel 2>/dev/null || echo "Database already exists"
psql -d cvm_tmcel -f db/init.sql

# Setup backend
echo "🐍 Setting up backend..."
cd backend
python -m venv venv

# Activate virtual environment (cross-platform)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt

# Generate mock data
echo "📝 Generating mock data..."
python generate_mock_data.py

cd ..

# Setup frontend
echo "⚛️ Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 To start the application:"
echo "1. Start the backend:"
echo "   cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Demo login credentials:"
echo "   Username: admin"
echo "   Password: admin"