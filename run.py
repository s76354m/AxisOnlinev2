import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Now run the application
if __name__ == "__main__":
    import streamlit.cli as stcli
    sys.argv = ["streamlit", "run", "app/ui/main.py"]
    sys.exit(stcli.main()) 