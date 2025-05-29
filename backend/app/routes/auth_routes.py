from flask import Blueprint, request, jsonify
from app.services import auth_service
import datetime

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
    
    # Get user role code
    role_code = 0  # Default to passenger
    
    # Format the response
    response = {
        "userID": user.user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": role_code,
        "createdAt": datetime.datetime.utcnow().isoformat() + "Z"
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