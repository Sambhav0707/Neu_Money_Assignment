"""
This file marks the 'app' directory as a Python package. 

By placing the Application Factory (`create_app`) here, we follow the 
official Flask best practices. This provides several benefits:
1. Clean Imports: We can cleanly import the app from anywhere via `from app import create_app`.
2. Encapsulation: The `app` directory itself acts as the central module.
"""

from flask import Flask
from app.config.settings import Config
from app.extensions import db

def create_app(config_class=Config):
    """
    Flask Application Factory.
    
    This function creates and configures the Flask app instance. 
    It is placed here to prevent circular imports: notice how blueprints 
    and error handlers are imported *inside* this function, ensuring the 
    app is fully initialized before the routes try to use it.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions (like the database)
    db.init_app(app)
    
    # Register error handlers
    # We import here to avoid circular dependencies
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register blueprints (routing)
    # We import here to avoid circular dependencies
    from app.controllers.employee_controller import employee_bp
    app.register_blueprint(employee_bp)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
        
    return app
