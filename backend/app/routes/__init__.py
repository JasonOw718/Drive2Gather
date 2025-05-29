from .auth_routes import auth_bp
from .ride_routes import ride_bp

def register_routes(app):
    """Register all route blueprints with the app"""
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ride_bp, url_prefix='/rides')
