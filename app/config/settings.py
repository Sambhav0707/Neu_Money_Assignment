"""
This file handles the application's configuration. It loads environment variables 
from the .env file and sets up configuration classes (like 'Config') that are 
used to configure the Flask application and its extensions (like the database URI).
"""

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
