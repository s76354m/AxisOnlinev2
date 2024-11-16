import os
import shutil
from pathlib import Path
import filecmp

def compare_and_merge_files(file1_path, file2_path):
    """Compare two files and keep the most up-to-date version."""
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        return
    
    # If files are identical, keep one and delete the other
    if filecmp.cmp(file1_path, file2_path, shallow=False):
        os.remove(file2_path)
    else:
        # Keep the more recently modified file
        stat1 = os.stat(file1_path)
        stat2 = os.stat(file2_path)
        if stat1.st_mtime > stat2.st_mtime:
            os.remove(file2_path)
        else:
            os.remove(file1_path)
            os.rename(file2_path, file1_path)

def cleanup_project():
    # Root directory is current directory
    root_dir = Path('.')
    
    # Files to compare and merge
    files_to_merge = [
        ('app/api/endpoints/yline.py', 'app/api/endpoints/y_line.py'),
        ('app/frontend/main.py', 'app/core/main.py'),
        ('app/main.py', 'app/frontend/main.py'),
        ('app/ui/main.py', 'app/frontend/app.py')
    ]
    
    # Directories to delete (empty or containing incorrect data)
    dirs_to_delete = [
        'app/database',
        'app/db/migrations',
        'app/db/seeders',
        'app/frontend/components',
        'app/models/base',
        'app/models/csp_lob',
        'app/models/project',
        'app/models/y_line',
        'app/services/base.py',
        'app/services/competitor',
        'app/services/csp_lob',
        'app/services/notes',
        'app/services/project',
        'app/services/service_area',
        'app/services/y_line',
        'app/ui/components/charts',
        'app/ui/components/common',
        'app/ui/components/forms',
        'app/ui/components/maps',
        'app/ui/components/tables',
        'app/ui/pages/competitor',
        'app/ui/pages/csp_lob',
        'app/ui/pages/dashboard',
        'app/ui/pages/notes',
        'app/ui/pages/project',
        'app/ui/pages/service_area',
        'app/ui/pages/y_line'
    ]
    
    # Files to delete
    files_to_delete = [
        'azure-pipelines.yml',
        'docker-compose.yml',
        'Dockerfile',
        'Dockerfile.test'
    ]
    
    # Step 1: Compare and merge files
    print("Comparing and merging files...")
    for file1, file2 in files_to_merge:
        try:
            compare_and_merge_files(
                os.path.join(root_dir, file1),
                os.path.join(root_dir, file2)
            )
            print(f"Processed: {file1} and {file2}")
        except Exception as e:
            print(f"Error processing {file1} and {file2}: {str(e)}")
    
    # Step 2: Delete directories
    print("\nDeleting empty/incorrect directories...")
    for dir_path in dirs_to_delete:
        try:
            full_path = os.path.join(root_dir, dir_path)
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                print(f"Deleted directory: {dir_path}")
        except Exception as e:
            print(f"Error deleting directory {dir_path}: {str(e)}")
    
    # Step 3: Delete files
    print("\nDeleting unnecessary files...")
    for file_path in files_to_delete:
        try:
            full_path = os.path.join(root_dir, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    
    # Step 4: Clean up __pycache__ directories
    print("\nCleaning up __pycache__ directories...")
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                try:
                    cache_path = os.path.join(root, dir_name)
                    shutil.rmtree(cache_path)
                    print(f"Deleted __pycache__: {cache_path}")
                except Exception as e:
                    print(f"Error deleting __pycache__ at {cache_path}: {str(e)}")

if __name__ == "__main__":
    print("Starting project cleanup...")
    cleanup_project()
    print("\nCleanup completed!") 