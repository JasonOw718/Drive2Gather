from flask import Blueprint, request, jsonify
from app.services import auth_service
import datetime
from app.utils.jwt_handler import token_required

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
    result, error = auth_service.send_password_reset_email(email)
    
    if error:
        return jsonify({"error": error}), 400
    
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