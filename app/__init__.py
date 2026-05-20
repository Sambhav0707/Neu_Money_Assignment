from flask import Flask
from app.config.settings import Config
from app.extensions import db, migrate

def create_app(config_class=Config):
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register blueprints
    from app.controllers.employee_controller import employee_bp
    app.register_blueprint(employee_bp)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
        
    return app
