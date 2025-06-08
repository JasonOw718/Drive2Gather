#!/usr/bin/env python
# create_admin.py

import os
import sys
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

# Add the app directory to the path so we can import from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from flask import Flask
from app.models import db, User, Admin
from app.routes import register_blueprints

def create_admin_user():
    """Create an admin user if it doesn't exist."""
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize the database
    db.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        
        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@drive2gather.com').first()
        
        if admin:
            # Admin already exists, exit
            return False
        
        # Create admin user
        admin_password = 'admin123'
        hashed_password = generate_password_hash(admin_password)
        
        # Create user record
        admin = User(
            name='Admin User',
            email='admin@drive2gather.com',
            password=hashed_password,
            phone_number='+60123456789',
            role='admin'
        )
        
        # Add and commit to database
        db.session.add(admin)
        db.session.commit()
        
        # Create admin record
        admin_record = Admin(
            user_id=admin.id
        )
        
        db.session.add(admin_record)
        db.session.commit()
        
        # Verify password was set correctly
        if check_password_hash(admin.password, admin_password):
            return True
        else:
            return None

if __name__ == '__main__':
    result = create_admin_user()
    sys.exit(0) 