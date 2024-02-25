from flask import Flask
from .routes.main_routes import bp as main_bp
from .routes.api_routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)    
    
    return app