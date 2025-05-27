from flask import Flask
from flask_cors import CORS
from .models import db
import os

def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS
    CORS(app)
    
    # Configure the SQLAlchemy database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URI', 'sqlite:///' + os.path.join(app.instance_path, 'drive2gather.sqlite')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')

    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize the database
    db.init_app(app)
    
    # Sample route to test the application
    @app.route('/')
    def index():
        return {'message': 'Welcome to Drive2Gather API!'}
    
    return app
