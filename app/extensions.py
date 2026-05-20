"""
This file centralizes the initialization of all Flask extensions (e.g., SQLAlchemy).
By creating the extension objects here without binding them to a specific Flask app, 
we avoid circular dependencies. The extensions are later bound to the app inside 
the Application Factory (app/__init__.py).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
