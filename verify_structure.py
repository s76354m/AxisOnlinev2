"""Script to verify project structure and required files"""
import os
from pathlib import Path
import sys

def verify_project_structure():
    """Verify all required files and directories exist"""
    # Define required structure
    required_structure = {
        'app': {
            '__init__.py': True,
            'models': {
                '__init__.py': True,
                'base.py': True,
                'project.py': True
            },
            'ui': {
                '__init__.py': True,
                'main.py': True,
                'pages': {
                    '__init__.py': True,
                    'dashboard.py': True,
                    'project_management.py': True,
                    'csp_lob_management.py': True,
                    'competitor_management.py': True,
                    'service_area_management.py': True,
                    'y_line_management.py': True
                }
            },
            'db': {
                '__init__.py': True,
                'base.py': True,
                'session.py': True
            },
            'utils': {
                '__init__.py': True,
                'validators.py': True
            }
        }
    }

    missing_files = []
    root_path = Path(__file__).parent

    def check_structure(structure, current_path):
        for item, value in structure.items():
            item_path = current_path / item
            if isinstance(value, dict):
                # It's a directory
                if not item_path.is_dir():
                    missing_files.append(f"Missing directory: {item_path}")
                else:
                    check_structure(value, item_path)
            else:
                # It's a file
                if not item_path.is_file():
                    missing_files.append(f"Missing file: {item_path}")

    check_structure(required_structure, root_path)

    if missing_files:
        print("❌ Project structure verification failed!")
        print("\nMissing files/directories:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ Project structure verification passed!")
        return True

def create_missing_files():
    """Create missing files with basic content"""
    base_files = {
        'app/__init__.py': '"""App package initialization"""',
        'app/models/__init__.py': '"""Models package initialization"""',
        'app/models/base.py': '''"""Base model for all database models"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
''',
        'app/ui/__init__.py': '"""UI package initialization"""',
        'app/ui/pages/__init__.py': '''"""UI pages initialization"""
from .dashboard import render_page as dashboard
from .project_management import render_page as project_management
from .csp_lob_management import render_page as csp_lob_management
from .competitor_management import render_page as competitor_management
from .service_area_management import render_page as service_area_management
from .y_line_management import render_page as y_line_management

__all__ = [
    'dashboard',
    'project_management',
    'csp_lob_management',
    'competitor_management',
    'service_area_management',
    'y_line_management'
]
''',
        'app/db/__init__.py': '"""Database package initialization"""',
        'app/utils/__init__.py': '"""Utils package initialization"""'
    }

    for file_path, content in base_files.items():
        path = Path(file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            print(f"Created: {file_path}")

if __name__ == "__main__":
    if not verify_project_structure():
        response = input("\nWould you like to create missing files with basic content? (y/n): ")
        if response.lower() == 'y':
            create_missing_files()
            verify_project_structure() 