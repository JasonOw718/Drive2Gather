from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO
from config import Config

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    from app.routes import register_routes
    register_routes(app)

    return app 