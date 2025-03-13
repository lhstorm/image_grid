#!/bin/bash

# Image Grid Drawing Tool - Launcher Script

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Image Grid Drawing Tool ===${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Warning: pip3 not found, trying pip...${NC}"
    if ! command -v pip &> /dev/null; then
        echo -e "${RED}Error: pip is not installed or not in PATH${NC}"
        echo "Please install pip and try again"
        exit 1
    fi
    PIP_CMD="pip"
else
    PIP_CMD="pip3"
fi

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}Checking dependencies...${NC}"
    
    # Check if streamlit is installed
    if ! python3 -c "import streamlit" &> /dev/null; then
        echo -e "${YELLOW}Streamlit not found. Installing dependencies...${NC}"
        $PIP_CMD install -r requirements.txt
        
        # Check if installation was successful
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to install dependencies${NC}"
            echo "Try running: $PIP_CMD install -r requirements.txt"
            exit 1
        fi
    else
        echo -e "${GREEN}Streamlit is already installed${NC}"
    fi
else
    echo -e "${YELLOW}Warning: requirements.txt not found${NC}"
    echo "Installing streamlit directly..."
    $PIP_CMD install streamlit opencv-python numpy matplotlib pillow
fi

# Check if the app file exists
if [ ! -f "streamlit_app.py" ]; then
    echo -e "${RED}Error: streamlit_app.py not found${NC}"
    echo "Make sure you're in the correct directory"
    exit 1
fi

# Run the Streamlit app
echo -e "${GREEN}Starting Image Grid Drawing Tool...${NC}"
echo "Press Ctrl+C to stop the app"
echo -e "${YELLOW}Opening browser window...${NC}"

# Run streamlit with error handling
streamlit run streamlit_app.py

# Check if streamlit exited with an error
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to start Streamlit app${NC}"
    echo "Check for errors in streamlit_app.py"
    exit 1
fi 