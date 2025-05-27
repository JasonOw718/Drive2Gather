from app import create_app
from app.models import db
from app.routes.auth_routes import auth_bp
import os

app = create_app()

# Register blueprints with prefix
app.register_blueprint(auth_bp, url_prefix='/auth')

# Ensure the instance folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'instance'), exist_ok=True)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
