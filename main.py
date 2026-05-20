"""
This is the entry point of the application. 
It uses the Application Factory to create the Flask app, establishes the 
database context (creating tables if they don't exist), and starts the 
development web server.
"""

import os
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Default to running on 0.0.0.0:5000 in development
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
