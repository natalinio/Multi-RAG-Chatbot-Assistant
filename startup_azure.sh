#!/bin/bash
set -e

echo "🚀 Starting CORTEX on Azure Web App..."

# 1. Navigate to the app root directory
cd /home/site/wwwroot

# 2. PERSISTENCE SETUP (The Fix)
# Instead of installing to system python (which resets on reboot),
# we create a virtual environment in /home/site/wwwroot/antenv.
# This directory is persisted by Azure Storage, so installs happen only once.
VENV_DIR="/home/site/wwwroot/antenv"

if [ ! -d "$VENV_DIR" ]; then
    echo "🌱 Creating persistent virtual environment in $VENV_DIR..."
    # Create venv using the system python
    python -m venv $VENV_DIR
else
    echo "✅ Persistent virtual environment found in $VENV_DIR."
fi

# 3. Activate the persistent environment
source $VENV_DIR/bin/activate

# 4. Install/Update Dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Checking dependencies (this takes time on first run)..."
    # pip will check installed packages in 'antenv' and skip if they exist.
    # This makes 2nd startup blazing fast.
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 5. Load environment variables
if [ -f ".env" ]; then
    echo "✅ Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

echo "🌐 Starting FastAPI with Uvicorn..."
PORT=${PORT:-8000}

# 6. Start the App using the VENV python
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT