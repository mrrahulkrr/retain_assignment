from flask import Flask
from models.database import init_db
from routes.health_routes import health_bp
from routes.shortener_routes import shortener_bp
from utils.error_handlers import register_error_handlers
import logging

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/')
    app.register_blueprint(shortener_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 