"""
Create an admin user for development and testing purposes.
Run this script to add an admin user to your database.

Usage:
python create_admin.py
"""

import sys
import os
from datetime import datetime

# Add the backend directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the Flask app from run.py
from flask import Flask
from app.models import db, User, UserRole, Admin
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

def create_admin_user():
    """Create an admin user if it doesn't exist"""
    # Setup a simple Flask app for this task
    app = Flask(__name__)
    config = Config()
    app.config.from_mapping(config.settings)
    db.init_app(app)
    
    with app.app_context():
        # Check if the admin user already exists
        existing_user = User.query.filter_by(email='admin@drive2gather.com').first()
        
        if existing_user:
            print("Admin user already exists!")
            return
        
        # Create the admin user
        admin_user = User(
            name="Admin User",
            email="admin@drive2gather.com",
            phone="1234567890",
            password=generate_password_hash("admin123")
        )
        
        # Add to database
        db.session.add(admin_user)
        db.session.flush()  # Get the user ID
        
        # Create admin role for the user
        admin_role = UserRole(role_name="admin")
        admin_role.user_id = admin_user.user_id
        db.session.add(admin_role)
        
        # Also add to Admin table
        admin_entry = Admin(user_id=admin_user.user_id)
        db.session.add(admin_entry)
        
        db.session.commit()
        
        # Now let's add a check_password method to the User class temporarily for testing
        def check_password(self, password):
            return check_password_hash(self.password, password)
        
        # Attach the method to the User class
        User.check_password = check_password
        
        # Test that it works
        test_user = User.query.filter_by(email='admin@drive2gather.com').first()
        if test_user and test_user.check_password("admin123"):
            print(f"Admin user created successfully and password verified!")
            print(f"Email: admin@drive2gather.com")
            print(f"Password: admin123")
        else:
            print("Warning: Admin created but password verification failed")
            print("You may need to add a check_password method to your User model")

if __name__ == "__main__":
    create_admin_user() 