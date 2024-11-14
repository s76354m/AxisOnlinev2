"""Main entry point for Streamlit application"""
import sys
from pathlib import Path

# Add the project root to Python path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

# Import the UI
from app.frontend.main import main

if __name__ == "__main__":
    main() 