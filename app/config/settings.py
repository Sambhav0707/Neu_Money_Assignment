import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost:5432/employee_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
