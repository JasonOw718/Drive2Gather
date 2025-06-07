from flask import Flask
from flask_cors import CORS
from app.models import db
from app import mail
from config import Config

# Initialize Config singleton
config = Config()

# Setup Flask application
app = Flask(__name__)
app.config.from_mapping(config.settings)

# Enable CORS
CORS(app)

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Register blueprints
from app.routes.auth_routes import auth_bp
from app.routes.ride_routes import ride_bp
from app.routes.notification_routes import notification_bp
from app.routes.chat_routes import chat_bp
from app.routes.donation_routes import donation_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(ride_bp, url_prefix='/api/rides')
app.register_blueprint(notification_bp, url_prefix='/api/notifications')
app.register_blueprint(chat_bp, url_prefix='/api/chats')
app.register_blueprint(donation_bp, url_prefix='/api/donations')




# Sample route to test the application
@app.route('/')
def index():
    return {'message': 'Welcome to Drive2Gather API!'}

if __name__ == '__main__':
    app.run(debug=config.get_config('DEBUG'))
