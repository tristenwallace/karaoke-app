import os
from flask import Flask
from .routes.main_routes import bp as main_bp
from .routes.api_routes import bp as api_bp
from .extensions import db, migrate
from .models import User, Session, Participant, SongsQueue, History
from flask.cli import with_appcontext
from .seed import seed_database  # Import the seed function
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    username = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    hostname = os.getenv('DATABASE_HOST')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{hostname}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("seed-db")  # Defines a new command: flask seed-db
    @with_appcontext
    def seed_db_command():
        """Seeds the database with initial data."""
        seed_database()


    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)    
    
    return app