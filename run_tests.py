"""Test runner script"""
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Now run the tests
if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["tests", "-v"])) 