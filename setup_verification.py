import sys
import subprocess
import importlib
from pathlib import Path
import os

class SetupVerification:
    def __init__(self):
        self.required_packages = [
            'fastapi',
            'sqlalchemy',
            'pyodbc',
            'streamlit',
            'pytest',
            'python-dotenv',
            'requests',
            'pydantic'
        ]
        self.required_files = [
            '.env',
            'app/db/session.py',
            'app/core/config.py',
            'app/models/project.py',
            'tests/test_db_connection.py'
        ]
        self.success_count = 0
        self.total_checks = 0

    def check_python_version(self):
        self.total_checks += 1
        print("\nChecking Python version...")
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            print(f"✅ Python version {version.major}.{version.minor} is compatible")
            self.success_count += 1
        else:
            print(f"❌ Python version {version.major}.{version.minor} is not compatible. Please use Python 3.8+")

    def check_packages(self):
        print("\nChecking required packages...")
        for package in self.required_packages:
            self.total_checks += 1
            try:
                importlib.import_module(package)
                print(f"✅ {package} is installed")
                self.success_count += 1
            except ImportError:
                print(f"❌ {package} is not installed")

    def check_files(self):
        print("\nChecking required files...")
        for file_path in self.required_files:
            self.total_checks += 1
            if Path(file_path).exists():
                print(f"✅ {file_path} exists")
                self.success_count += 1
            else:
                print(f"❌ {file_path} is missing")

    def check_database_connection(self):
        self.total_checks += 1
        print("\nChecking database connection...")
        try:
            from app.db.session import engine
            with engine.connect() as connection:
                result = connection.execute("SELECT 1").scalar()
                if result == 1:
                    print("✅ Database connection successful")
                    self.success_count += 1
                else:
                    print("❌ Database connection failed")
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")

    def check_environment_variables(self):
        self.total_checks += 1
        print("\nChecking environment variables...")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            required_vars = ['DB_SERVER', 'DB_NAME', 'DB_DRIVER']
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            
            if not missing_vars:
                print("✅ All required environment variables are set")
                self.success_count += 1
            else:
                print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        except Exception as e:
            print(f"❌ Error checking environment variables: {str(e)}")

    def check_project_structure(self):
        self.total_checks += 1
        print("\nChecking project structure...")
        required_dirs = ['app', 'tests', 'app/models', 'app/db', 'app/core']
        missing_dirs = [dir for dir in required_dirs if not Path(dir).is_dir()]
        
        if not missing_dirs:
            print("✅ Project structure is correct")
            self.success_count += 1
        else:
            print(f"❌ Missing directories: {', '.join(missing_dirs)}")

    def run_basic_test(self):
        self.total_checks += 1
        print("\nAttempting to run a basic test...")
        try:
            result = subprocess.run(
                ['pytest', 'tests/test_db_connection.py', '-v'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Basic test passed")
                self.success_count += 1
            else:
                print(f"❌ Basic test failed:\n{result.stderr}")
        except Exception as e:
            print(f"❌ Error running test: {str(e)}")

    def run_all_checks(self):
        print("Starting setup verification...\n")
        self.check_python_version()
        self.check_packages()
        self.check_files()
        self.check_project_structure()
        self.check_environment_variables()
        self.check_database_connection()
        self.run_basic_test()

        print(f"\nVerification complete: {self.success_count}/{self.total_checks} checks passed")
        
        if self.success_count == self.total_checks:
            print("\n✅ All checks passed! You can proceed with running the tests.")
        else:
            print(f"\n❌ {self.total_checks - self.success_count} checks failed. Please fix the issues above before running tests.")

if __name__ == "__main__":
    verifier = SetupVerification()
    verifier.run_all_checks() 