import jwt
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, UserRole, Driver, Passenger, db
from flask import current_app

def register_user(name, email, phone, password):
    """Register a new user"""
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    # Create new user
    hashed_password = generate_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password=hashed_password
    )
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

def login_user(email, password):
    """Authenticate a user and return JWT"""
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return None, "Invalid email or password"
    
    # Get user role
    user_role = UserRole.query.filter_by(user_id=user.user_id).first()
    role_code = get_role_code(user_role.role_name) if user_role else 0

    # Generate token
    token = generate_token(user)
    
    return {
        "token": token,
        "expiresIn": 3600,
        "user": {
            "userID": user.user_id,
            "name": user.name,
            "role": role_code
        }
    }, None

def register_driver(name, email, phone, password, license_number, car_number, car_type, car_color):
    """Register a new driver (creates user + promotes to driver)"""
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    # Create new user
    hashed_password = generate_password_hash(password)
    new_user = User(
        name=name,
        email=email,
        phone=phone,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.flush()  # Get the user_id before commit
    
    # Add driver role
    role = UserRole(role_name="driver")
    role.user_id = new_user.user_id
    db.session.add(role)
    
    # Create driver profile
    driver = Driver(
        user_id=new_user.user_id,
        license_number=license_number,
        car_number=car_number,
        car_type=car_type,
        car_color=car_color
    )
    db.session.add(driver)
    
    db.session.commit()
    
    return {
        "userID": new_user.user_id,
        "name": new_user.name,
        "email": new_user.email,
        "phone": new_user.phone,
        "role": 2,  # Driver role code
        "licenseNumber": driver.license_number,
        "carNumber": driver.car_number,
        "carType": driver.car_type,
        "carColour": driver.car_color,
        "createdAt": datetime.datetime.utcnow().isoformat() + "Z"
    }, None

def generate_token(user):
    """Generate JWT token"""
    payload = {
        'sub': user.user_id,
        'name': user.name,
        'email': user.email,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

def get_role_code(role_name):
    """Convert role name to numeric code"""
    role_codes = {
        "passenger": 0,
        "donor": 1,
        "driver": 2,
        "admin": 3
    }
    return role_codes.get(role_name, 0) 