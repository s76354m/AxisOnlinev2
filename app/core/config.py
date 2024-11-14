from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Axis Program Management"
    
    # Database settings
    DB_SERVER: str = os.getenv("DB_SERVER", "DESKTOP-PJTAP42\\SQLEXPRESS")
    DB_NAME: str = os.getenv("DB_NAME", "ndar")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC+Driver+17+for+SQL+Server")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"mssql+pyodbc://{self.DB_SERVER}/{self.DB_NAME}?"
            f"driver={self.DB_DRIVER}&trusted_connection=yes"
        )

settings = Settings() 