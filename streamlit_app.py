"""Main entry point for Streamlit application"""
import sys
from pathlib import Path

# Add project root to Python path
root_path = Path(__file__).parent
sys.path.append(str(root_path))

from app.ui.main import main

if __name__ == "__main__":
    main() 