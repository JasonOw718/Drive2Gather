import jwt
import datetime
import logging
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, UserRole, Driver, Passenger, db
from flask import current_app
from flask_mail import Message
from app import mail

# Configure logging
logger = logging.getLogger('auth_service')

def register_user(name, email, phone, password):
    """Register a new user"""
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    # Use Builder pattern to create user
    from app.utils.builders import UserBuilder, Director
    
    user_builder = UserBuilder()
    director = Director(user_builder)
    
    user_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'password': password,
        'role': 'passenger'
    }
    
    try:
        new_user = director.construct_user(user_data)
        db.session.add(new_user)
        db.session.flush()  # Get the user_id before commit
        
        # Add default passenger role
        role = UserRole(role_name="passenger")
        role.user_id = new_user.user_id
        db.session.add(role)
        
        # Create passenger profile
        passenger = Passenger(user_id=new_user.user_id)
        db.session.add(passenger)
        
        db.session.commit()
        
        return new_user, None
        
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def login_user(email, password):
    """Authenticate a user and return JWT"""
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return None, "Invalid email or password"
    
    # Get user role
    user_role = UserRole.query.filter_by(user_id=user.user_id).first()
    role_name = user_role.role_name if user_role else "passenger"

    # If the user is a driver, check verification status
    if role_name == "driver":
        driver = Driver.query.filter_by(user_id=user.user_id).first()
        if driver and driver.verification_status != "approved":
            return None, f"Your driver account is still {driver.verification_status}. Please wait for admin approval."

    # Generate token
    token = generate_token(user)
    
    return {
        "token": token,
        "expiresIn": 3600,
        "user": {
            "name": user.name,
            "role": role_name
        }
    }, None

def change_password(user_id, old_password, new_password):
    """
    Change user password
    
    Args:
        user_id (str): User ID
        old_password (str): Current password
        new_password (str): New password
        
    Returns:
        tuple: (success, error)
    """
    try:
        # Get user by ID
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not check_password_hash(user.password, old_password):
            return False, "Current password is incorrect"
        
        # Validate new password (you might want to add more validation rules)
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long"
        
        # Hash and update the new password
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def send_password_reset_email(email):
    """
    Send a password reset email
    
    Args:
        email (str): User's email address
        
    Returns:
        tuple: (success, error)
    """
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return False, "Email not registered"
    
    try:
        # In a real app, you would generate a secure token and include it in the URL
        # For this simplified version, we're just sending a dummy email
        reset_url = "https://drive2gather.com/reset-password?dummy=1"
        
        # Create message
        msg = Message(
            subject="Drive2Gather Password Reset",
            recipients=[email],
            body=f"""
Hello {user.name},

You have requested to reset your password. Please click on the link below to reset your password:

{reset_url}

If you did not request a password reset, please ignore this email.

Best regards,
Drive2Gather Team
            """,
            html=f"""
<p>Hello {user.name},</p>
<p>You have requested to reset your password. Please click on the link below to reset your password:</p>
<p><a href="{reset_url}">Reset Password</a></p>
<p>If you did not request a password reset, please ignore this email.</p>
<p>Best regards,<br>Drive2Gather Team</p>
            """
        )
        
        # Send email
        mail.send(msg)
        
        return True, None
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def register_driver(name, email, phone, password, license_number, car_number, car_type, car_color):
    """Register a new driver (creates user + promotes to driver)"""
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    # Use Builder pattern to create driver
    from app.utils.builders import DriverBuilder, Director
    
    driver_builder = DriverBuilder()
    director = Director(driver_builder)
    
    driver_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'password': password,
        'license_number': license_number,
        'car_number': car_number,
        'car_type': car_type,
        'car_color': car_color
    }
    
    new_user, driver = director.construct_driver(driver_data)
    
    try:
        # Add user to the database first
        db.session.add(new_user)
        db.session.flush()  # Get the user_id before creating other objects
        
        # Now that we have the user_id, ensure it's set in the driver
        driver.user_id = new_user.user_id
        
        # Add driver role
        role = UserRole(role_name="driver")
        role.user_id = new_user.user_id
        db.session.add(role)
        
        # Add driver profile
        db.session.add(driver)
        
        db.session.commit()
        
        return {
            "name": new_user.name,
            "email": new_user.email,
            "phone": new_user.phone,
            "role": "driver",
            "licenseNumber": driver.license_number,
            "carNumber": driver.car_number,
            "carType": driver.car_type,
            "carColour": driver.car_color
        }, None
        
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def generate_token(user):
    """Generate JWT token"""
    logger.info(f"Generating token for user: {user.user_id} ({user.name})")
    
    payload = {
        'sub': str(user.user_id),  # Convert user_id to string to satisfy PyJWT requirements
        'name': user.name,
        'email': user.email,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    
    logger.info(f"Token payload: {payload}")
    
    secret_key = current_app.config.get('SECRET_KEY')
    logger.info(f"Using SECRET_KEY: {secret_key[:5]}..." if secret_key else "SECRET_KEY is None!")
    
    try:
        token = jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )
        logger.info(f"Token generated successfully: {token[:10]}...{token[-10:] if len(token) > 20 else ''}")
        return token
    except Exception as e:
        logger.error(f"Error generating token: {str(e)}")
        raise

def get_role_code(role_name):
    """Convert role name to numeric code"""
    role_codes = {
        "passenger": 0,
        "donor": 1,
        "driver": 2,
        "admin": 3
    }
    return role_codes.get(role_name, 0)

def get_user_profile(user_id):
    """
    Get user profile information
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        tuple: (user_data, error)
    """
    try:
        # Get the user
        user = User.query.get(user_id)
        if not user:
            return None, f"User with ID {user_id} not found"
        
        # Get user role
        user_role = UserRole.query.filter_by(user_id=user_id).first()
        role_name = user_role.role_name if user_role else "passenger"
        
        # Basic user data
        user_data = {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": role_name
        }
        
        # Add role-specific data
        if role_name == "driver":
            driver = Driver.query.filter_by(user_id=user_id).first()
            if driver:
                user_data.update({
                    "license_number": driver.license_number,
                    "car_number": driver.car_number,
                    "car_type": driver.car_type,
                    "car_color": driver.car_color
                })
                
                # Add donation information for drivers
                from sqlalchemy import func
                from app.models import Donation
                
                # Get total donations received
                total_donations = db.session.query(func.sum(Donation.amount)).filter(Donation.user_id == user_id).scalar() or 0
                
                # Get count of donations received
                donation_count = db.session.query(Donation).filter(Donation.user_id == user_id).count()
                
                user_data.update({
                    "total_donations": float(total_donations),
                    "donation_count": donation_count
                })
        
        return user_data, None
    except Exception as e:
        return None, str(e) 