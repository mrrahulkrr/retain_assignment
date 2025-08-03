# Refactored clean version
from flask import Flask
from config import Config
from models.database import init_db
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from utils.error_handlers import register_error_handlers
import logging

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'User Management API is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
