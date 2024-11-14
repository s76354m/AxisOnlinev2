from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_SERVER: str = os.getenv("DB_SERVER", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_ECHO: bool = os.getenv("DB_ECHO", "False").lower() == "true"
    DB_TRUSTED_CONNECTION: bool = True

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Axis Program Management"

    class Config:
        case_sensitive = True

    @property
    def DATABASE_URL(self) -> str:
        """Constructs the database URL for Windows Authentication"""
        # Clean up the driver name
        driver = self.DB_DRIVER.replace('+', ' ')
        
        # Construct the connection string
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            "Trusted_Connection=yes;"
        )
        
        # URL encode the connection string
        params = urllib.parse.quote_plus(conn_str)
        
        return f"mssql+pyodbc:///?odbc_connect={params}"

settings = Settings() 