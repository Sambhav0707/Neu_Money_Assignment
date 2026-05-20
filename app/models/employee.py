"""
This file defines the Database Models (SQLAlchemy). 
These models are pure data representations that map directly to database tables. 
They do NOT contain any business logic or HTTP-related code.
"""

from datetime import datetime, timezone
from app.extensions import db

class Employee(db.Model):
    """
    SQLAlchemy model representing the 'employees' table.
    This model contains NO business logic, only data representation.
    """
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False)
    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Audit timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, name='{self.name}', email='{self.email}')>"
