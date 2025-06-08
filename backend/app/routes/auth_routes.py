from flask import Blueprint, request, jsonify
from app.services import auth_service
import datetime
from app.utils.jwt_handler import token_required
import jwt
from flask import current_app
from datetime import datetime, timedelta
from app.models.user import User,UserRole
from app.models import db, Donor
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users', methods=['POST'])
def signup():
    """Create a new user"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Register the user
    user, error = auth_service.register_user(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Format the response
    response = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": "passenger"
    }
    
    return jsonify(response), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and return JWT"""
    data = request.json
    
    # Validate required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    email = data['email']
    password = data['password']
    
    # Look up the user with the provided email
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
        
    # Check if user has admin or donor role (these users should use their specific login endpoints)
    admin_role = UserRole.query.filter_by(user_id=user.user_id, role_name='admin').first()
    donor_role = UserRole.query.filter_by(user_id=user.user_id, role_name='donor').first()
    
    if admin_role:
        return jsonify({"error": "Admin users must use the admin login endpoint"}), 403
        
    if donor_role:
        return jsonify({"error": "Donor users must use the donor login endpoint"}), 403
    
    # Verify password
    if not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Authenticate the user
    auth_data, error = auth_service.login_user(
        email=data['email'],
        password=data['password']
    )
    
    if error:
        return jsonify({"error": error}), 401
    
    return jsonify(auth_data), 200

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password"""
    data = request.json
    
    # Validate required fields
    required_fields = ['userId', 'oldPassword', 'newPassword']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Change password
    success, error = auth_service.change_password(
        user_id=data['userId'],
        old_password=data['oldPassword'],
        new_password=data['newPassword']
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "Password changed successfully"}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    data = request.json
    
    # Validate required fields
    if 'email' not in data:
        return jsonify({"error": "Missing required field: email"}), 400
    
    # Check if user exists
    email = data['email']
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Email not registered"}), 404
    
    # Generate reset token
    import secrets
    token = secrets.token_urlsafe(32)
    
    # Store token in database or session for verification later
    # This is a simplified implementation. In production, you'd store this securely
    # with an expiration time, hashed, etc.
    
    # Send reset email
    result = auth_service.send_password_reset_email(user, token)
    
    if not result:
        return jsonify({"error": "Failed to send password reset email"}), 500
    
    return jsonify({"message": "Password reset email sent successfully"}), 200

@auth_bp.route('/drivers', methods=['POST'])
def signup_driver():
    """Create a new driver account"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'phone', 'password', 
                      'licenseNumber', 'carNumber', 'carType', 'carColour']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Register the driver
    driver_data, error = auth_service.register_driver(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password'],
        license_number=data['licenseNumber'],
        car_number=data['carNumber'],
        car_type=data['carType'],
        car_color=data['carColour']
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(driver_data), 201

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get the current user's profile information"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Get user profile
    user_data, error = auth_service.get_user_profile(user_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(user_data), 200

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(user_id):
    """Get a user's profile information by ID"""
    # Get user profile
    user_data, error = auth_service.get_user_profile(user_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(user_data), 200

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint - also handles donor login requests"""
    data = request.json
    
    # Validate request body
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    email = data['email']
    password = data['password']
    user_type = data.get('userType', 'admin')  # Default to admin if not specified
    
    # Look up the user with the provided email
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Verify password
    if not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Check if user has appropriate role based on userType
    if user_type == 'donor':
        # Check for donor role
        role = UserRole.query.filter_by(user_id=user.user_id, role_name='donor').first()
        if not role:
            return jsonify({"error": "Unauthorized: Not a donor"}), 403
        
        # Generate JWT token for donor
        token_payload = {
            'sub': user.user_id,
            'email': user.email,
            'is_donor': True,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "token": token,
            "expiresIn": 86400,  # 24 hours in seconds
            "donor": {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": "donor"
            }
        }), 200
    else:
        # Check for admin role
        admin_role = UserRole.query.filter_by(user_id=user.user_id, role_name='admin').first()
        
        if not admin_role:
            return jsonify({"error": "Unauthorized: Not an admin"}), 403
        
        # Generate JWT token for admin
        token_payload = {
            'sub': user.user_id,
            'email': user.email,
            'is_admin': True,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "token": token,
            "expiresIn": 86400,  # 24 hours in seconds
            "admin": {
                "id": user.user_id,
                "name": user.name,
                "email": user.email,
                "role": "admin"
            }
        }), 200

@auth_bp.route('/admin/register', methods=['POST'])
def admin_register():
    """Admin register endpoint - also handles donor registration"""
    data = request.json
    
    # Validate request body
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'phone', 'userType']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    user_type = data['userType']  # 'admin' or 'donor'
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400
    
    try:
        # Create new user
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.flush()  # Get the user_id before commit
        
        # Add role based on userType
        if user_type == 'donor':
            # Add donor role
            role = UserRole(role_name="donor")
            role.user_id = new_user.user_id
            db.session.add(role)
            
            # Create donor profile
            donor = Donor(user_id=new_user.user_id)
            db.session.add(donor)
            
            db.session.commit()
            
            # Generate JWT token
            token_payload = {
                'sub': new_user.user_id,
                'email': new_user.email,
                'is_donor': True,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            
            token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                "token": token,
                "expiresIn": 86400,  # 24 hours in seconds
                "donor": {
                    "id": new_user.user_id,
                    "name": new_user.name,
                    "email": new_user.email,
                    "phone": new_user.phone,
                    "role": "donor"
                }
            }), 201
        elif user_type == 'admin':
            # Add admin role
            role = UserRole(role_name="admin")
            role.user_id = new_user.user_id
            db.session.add(role)
            
            db.session.commit()
            
            # Generate JWT token
            token_payload = {
                'sub': new_user.user_id,
                'email': new_user.email,
                'is_admin': True,
                'exp': datetime.utcnow() + timedelta(hours=24)
            }
            
            token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                "token": token,
                "expiresIn": 86400,  # 24 hours in seconds
                "admin": {
                    "id": new_user.user_id,
                    "name": new_user.name,
                    "email": new_user.email,
                    "role": "admin"
                }
            }), 201
        else:
            db.session.rollback()
            return jsonify({"error": f"Invalid user type: {user_type}"}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/donor/register', methods=['POST'])
def donor_register():
    """Register a new donor"""
    data = request.json
    
    # Validate request body
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400
    
    try:
        # Create new user
        new_user = User(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.flush()  # Get the user_id before commit
        
        # Add donor role
        role = UserRole(role_name="donor")
        role.user_id = new_user.user_id
        db.session.add(role)
        
        # Create donor profile
        donor = Donor(user_id=new_user.user_id)
        db.session.add(donor)
        
        db.session.commit()
        
        # Generate JWT token
        token_payload = {
            'sub': new_user.user_id,
            'email': new_user.email,
            'is_donor': True,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            "token": token,
            "expiresIn": 86400,  # 24 hours in seconds
            "donor": {
                "id": new_user.user_id,
                "name": new_user.name,
                "email": new_user.email,
                "phone": new_user.phone,
                "role": "donor"
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/donor/login', methods=['POST'])
def donor_login():
    """Donor login endpoint"""
    data = request.json
    
    # Validate request body
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400
    
    email = data['email']
    password = data['password']
    
    # Look up the user with the provided email
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Check if user has donor role
    donor_role = UserRole.query.filter_by(user_id=user.user_id, role_name='donor').first()
    
    if not donor_role:
        return jsonify({"error": "Unauthorized: Not a donor"}), 403
    
    # Verify password
    if not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Generate JWT token
    token_payload = {
        'sub': user.user_id,
        'email': user.email,
        'is_donor': True,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        "token": token,
        "expiresIn": 86400,  # 24 hours in seconds
        "donor": {
            "id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": "donor"
        }
    }), 200 

@auth_bp.route('/donors/profile', methods=['GET'])
@token_required
def get_donor_profile():
    """Get the current donor's profile information"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Get user profile
    user_data, error = auth_service.get_user_profile(user_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    # Check if user has donor role
    donor_role = UserRole.query.filter_by(user_id=user_id, role_name='donor').first()
    
    if not donor_role:
        return jsonify({"error": "Unauthorized: Not a donor"}), 403
    
    return jsonify(user_data), 200

@auth_bp.route('/donors/profile', methods=['PUT'])
@token_required
def update_donor_profile():
    """Update the current donor's profile information"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Check if user has donor role
    donor_role = UserRole.query.filter_by(user_id=user_id, role_name='donor').first()
    
    if not donor_role:
        return jsonify({"error": "Unauthorized: Not a donor"}), 403
    
    # Get request data
    data = request.json
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    # Update user
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Update fields
    if 'name' in data:
        user.name = data['name']
    
    if 'phone' in data:
        user.phone = data['phone']
    
    try:
        db.session.commit()
        
        # Return updated user data
        return jsonify({
            "id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": "donor"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

@auth_bp.route('/donors/password', methods=['PUT'])
@token_required
def change_donor_password():
    """Change donor password"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Check if user has donor role
    donor_role = UserRole.query.filter_by(user_id=user_id, role_name='donor').first()
    
    if not donor_role:
        return jsonify({"error": "Unauthorized: Not a donor"}), 403
    
    # Get request data
    data = request.json
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    # Validate required fields
    if 'currentPassword' not in data or 'newPassword' not in data:
        return jsonify({"error": "Current password and new password are required"}), 400
    
    # Get user
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Check current password
    if not user.check_password(data['currentPassword']):
        return jsonify({"error": "Current password is incorrect"}), 400
    
    # Validate new password
    if len(data['newPassword']) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    # Change password
    user.password = generate_password_hash(data['newPassword'])
    
    try:
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to change password: {str(e)}"}), 500 