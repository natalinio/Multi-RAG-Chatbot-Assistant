#!/bin/bash
# Startup script for ETL Assistant Chatbot
# This script sets up the environment and starts the FastAPI application

set -e  # Exit on any error

echo "🚀 Starting ETL Assistant Chatbot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
}

# Check if virtual environment exists
setup_virtual_environment() {
    print_status "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # macOS/Linux
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Check environment variables
check_environment() {
    print_status "Checking environment configuration..."
    
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            print_warning ".env file not found. Please copy .env.example to .env and configure your Azure credentials."
            print_status "Creating .env from .env.example..."
            cp .env.example .env
            print_warning "Please edit .env file with your Azure service credentials before continuing."
            read -p "Press Enter to continue once you've configured .env file..."
        else
            print_error ".env file not found and no .env.example available"
            exit 1
        fi
    else
        print_success ".env file found"
    fi
    
    # Source environment variables
    if [ -f ".env" ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    # Check critical environment variables
    REQUIRED_VARS=(
        "AZURE_OPENAI_ENDPOINT"
        "AZURE_OPENAI_API_KEY" 
        "AZURE_OPENAI_DEPLOYMENT_NAME"
        "COSMOS_DB_ENDPOINT"
        "COSMOS_DB_KEY"
        "COSMOS_DB_DATABASE_NAME"
        "COSMOS_DB_CONTAINER_NAME"
    )
    
    MISSING_VARS=()
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            MISSING_VARS+=("$var")
        fi
    done
    
    if [ ${#MISSING_VARS[@]} -ne 0 ]; then
        print_error "Missing required environment variables:"
        for var in "${MISSING_VARS[@]}"; do
            echo "  - $var"
        done
        print_error "Please configure these variables in your .env file"
        exit 1
    fi
    
    print_success "Environment configuration validated"
}

# Health check
health_check() {
    print_status "Performing health check..."
    
    # Wait a moment for the server to start
    sleep 3
    
    # Check if the server is responding
    if command -v curl &> /dev/null; then
        HEALTH_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:8000/api/health -o /dev/null || echo "000")
        if [ "$HEALTH_RESPONSE" = "200" ]; then
            print_success "Health check passed - API is responding"
        else
            print_warning "Health check failed - API may still be starting up"
        fi
    else
        print_warning "curl not available - skipping health check"
    fi
}

# Start the application
start_application() {
    print_status "Starting FastAPI application..."
    
    # Set default values
    HOST=${HOST:-"0.0.0.0"}
    PORT=${PORT:-8000}
    
    print_status "Server will start on http://$HOST:$PORT"
    print_status "API documentation will be available at http://$HOST:$PORT/docs"
    print_status "Web interface will be available at http://$HOST:$PORT"
    
    # Start the server
    if command -v uvicorn &> /dev/null; then
        print_success "Starting server with uvicorn..."
        
        # Run health check in background after delay
        (sleep 5 && health_check) &
        
        # Start the main application
        uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
    else
        print_error "uvicorn not found. Please ensure it's installed via requirements.txt"
        exit 1
    fi
}

# Cleanup function
cleanup() {
    print_status "Shutting down gracefully..."
    exit 0
}

# Trap signals for cleanup
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "========================================="
    echo "ETL Assistant Chatbot Startup Script"
    echo "========================================="
    echo ""
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Run setup steps
    check_python
    setup_virtual_environment
    install_dependencies
    check_environment
    
    echo ""
    print_success "Setup completed successfully!"
    echo ""
    print_status "Starting application..."
    echo ""
    
    # Start the application
    start_application
}

# Parse command line arguments
case "${1:-}" in
    --help|-h)
        echo "ETL Assistant Chatbot Startup Script"
        echo ""
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --help, -h          Show this help message"
        echo "  --check-only        Only perform environment checks"
        echo "  --install-only      Only install dependencies"
        echo ""
        echo "Environment Variables:"
        echo "  HOST                Server host (default: 0.0.0.0)"
        echo "  PORT                Server port (default: 8000)"
        echo ""
        exit 0
        ;;
    --check-only)
        check_python
        check_environment
        print_success "Environment check completed"
        exit 0
        ;;
    --install-only)
        check_python
        setup_virtual_environment
        install_dependencies
        print_success "Installation completed"
        exit 0
        ;;
    "")
        # Run normally
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac