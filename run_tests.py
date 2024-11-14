"""Test runner script"""
import subprocess
import datetime
import sys
import os

def run_tests():
    """Run tests and capture output"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"test_results_{timestamp}.txt"
    
    try:
        # Create test results directory if it doesn't exist
        os.makedirs("test_results", exist_ok=True)
        output_path = os.path.join("test_results", output_file)
        
        # Run pytest with coverage and capture output
        result = subprocess.run(
            [
                "pytest",
                "--cov=app",
                "--cov-report=term-missing",
                "--verbose",
                "--tb=short"
            ],
            capture_output=True,
            text=True
        )
        
        # Write output to file
        with open(output_path, "w") as f:
            f.write("TEST RESULTS\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date: {datetime.datetime.now()}\n")
            f.write("=" * 80 + "\n\n")
            
            # Write test output
            f.write(result.stdout)
            
            # Write errors if any
            if result.stderr:
                f.write("\nERRORS AND WARNINGS\n")
                f.write("=" * 80 + "\n")
                f.write(result.stderr)
            
            # Write summary
            f.write("\nTEST SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Return Code: {result.returncode}\n")
            f.write(f"Tests Run At: {datetime.datetime.now()}\n")
            
        print(f"Test results written to {output_path}")
        
        # Print summary to console
        print("\nTest Summary:")
        print("-" * 40)
        print(f"Return Code: {result.returncode}")
        if result.returncode != 0:
            print("Some tests failed. Check the output file for details.")
        
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests()) 