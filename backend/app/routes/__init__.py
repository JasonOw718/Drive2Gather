from .auth_routes import auth_bp
from .ride_routes import ride_bp
from .notification_routes import notification_bp
from .chat_routes import chat_bp
from .donation_routes import donation_bp
from .admin_routes import admin_bp
from .feedback_routes import feedback_bp

def register_routes(app):
    """Register all route blueprints with the app"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ride_bp, url_prefix='/rides')
    app.register_blueprint(notification_bp, url_prefix='/notifications')
    app.register_blueprint(chat_bp, url_prefix='/chats')
    app.register_blueprint(donation_bp, url_prefix='/donations')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
