import os
from dotenv import load_dotenv

def check_environment():
    load_dotenv()
    
    required_vars = ['DB_SERVER', 'DB_NAME', 'DB_DRIVER']
    
    print("Environment Variables:")
    for var in required_vars:
        value = os.getenv(var)
        print(f"{var}: {'[SET]' if value else '[MISSING]'}")
        if value:
            print(f"  Value: {value}")

if __name__ == "__main__":
    check_environment() 