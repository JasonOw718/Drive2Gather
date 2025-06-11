from flask import Flask
from flask_cors import CORS
from app.models import db, User, UserRole, Admin
from app import mail
from config import Config
from werkzeug.security import generate_password_hash

# Initialize Config singleton
config = Config()

# Setup Flask application
app = Flask(__name__)
app.config.from_mapping(config.settings)

# Enable CORS with specific configurations that work for all requests including OPTIONS/preflight
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://jasonow718.github.io"]}})

# Initialize extensions
db.init_app(app)
mail.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    admin_email = "admin@ride2gather.com"
    admin = User.query.filter_by(email=admin_email).first()
    
    if not admin:
        print("Creating admin user...")
        # Create a new admin user
        admin = User(
            name="Admin User",
            email=admin_email,
            phone="1234567890",
            password=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()
        
        # Add admin role
        admin_role = UserRole(role_name="admin")
        admin_role.user_id = admin.user_id
        db.session.add(admin_role)
        
        # Add admin profile
        admin_profile = Admin()
        admin_profile.user_id = admin.user_id
        db.session.add(admin_profile)
        
        db.session.commit()
        print(f"Admin user created with email: {admin_email} and password: admin123")

# Register blueprints
from app.routes.auth_routes import auth_bp
from app.routes.ride_routes import ride_bp
from app.routes.notification_routes import notification_bp
from app.routes.chat_routes import chat_bp
from app.routes.donation_routes import donation_bp
from app.routes.admin_routes import admin_bp
from app.routes.feedback_routes import feedback_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(ride_bp, url_prefix='/api/rides')
app.register_blueprint(notification_bp, url_prefix='/api/notifications')
app.register_blueprint(chat_bp, url_prefix='/api/chats')
app.register_blueprint(donation_bp, url_prefix='/api/donations')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(feedback_bp, url_prefix='/api/feedback')


# Sample route to test the application
@app.route('/')
def index():
    return {'message': 'Welcome to Ride2Gather API!'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.get_config('DEBUG'))