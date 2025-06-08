import jwt
import logging
import inspect
from functools import wraps
from flask import request, jsonify, current_app, g
from app.models import User, UserRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('jwt_handler')

def get_token_from_header():
    """Extract token from the Authorization header"""
    auth_header = request.headers.get('Authorization')
    logger.info(f"Authorization header: {auth_header[:15] + '...' if auth_header else 'None'}")
    if not auth_header or 'Bearer ' not in auth_header:
        logger.warning("No Bearer token found in Authorization header")
        return None
    token = auth_header.split('Bearer ')[1]
    logger.info(f"Token extracted: {token[:10]}...{token[-10:] if len(token) > 20 else ''}")
    return token

def decode_token(token):
    """Decode and validate the JWT token"""
    logger.info(f"Attempting to decode token: {token[:10]}...{token[-10:] if len(token) > 20 else ''}")
    try:
        secret_key = current_app.config.get('SECRET_KEY')
        logger.info(f"Using SECRET_KEY: {secret_key[:5]}..." if secret_key else "SECRET_KEY is None!")
        
        payload = jwt.decode(
            token, 
            secret_key,
            algorithms=['HS256']
        )
        logger.info(f"Token decoded successfully. Payload contains keys: {list(payload.keys())}")
        return payload, None
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token expired: {str(e)}")
        return None, "Token has expired"
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        return None, "Invalid token"
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {str(e)}")
        return None, f"Token validation error: {str(e)}"

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.info(f"Request to protected endpoint: {request.method} {request.path}")
        token = get_token_from_header()
        
        if not token:
            logger.warning("Token missing in request")
            return jsonify({"error": "Token is missing"}), 401
        
        payload, error = decode_token(token)
        if error:
            logger.warning(f"Token validation failed: {error}")
            return jsonify({"error": error}), 401
        
        # Get the user
        try:
            # Check if 'sub' exists in payload
            if 'sub' not in payload:
                logger.error("Token payload missing 'sub' field")
                return jsonify({"error": "Invalid token: missing user ID"}), 401
                
            # Try to convert the user_id to int, with better error handling
            try:
                user_id = int(payload['sub'])
            except (ValueError, TypeError):
                logger.error(f"Failed to convert user_id to integer: {payload['sub']}")
                return jsonify({"error": "Invalid user ID format in token"}), 401
                
            logger.info(f"Looking up user with ID: {user_id}")
            user = User.query.filter_by(user_id=user_id).first()
            
            if not user:
                logger.warning(f"User not found for user_id: {user_id}")
                return jsonify({"error": "User not found"}), 404
                
            logger.info(f"User authenticated: {user.user_id} ({user.name})")
            # Add the user to the request context
            request.user = user
            
            # Also set in Flask g object for compatibility
            g.user = user
            
            # Check if the function expects a current_user parameter
            sig = inspect.signature(f)
            if 'current_user' in sig.parameters:
                # Pass the authenticated user as the current_user parameter
                kwargs['current_user'] = user
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error processing token: {str(e)}")
            return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    return decorated

def role_required(roles):
    """Decorator to restrict access based on user role"""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated_function(*args, **kwargs):
            user = request.user  # Always use request.user for role checks
            user_roles = UserRole.query.filter_by(user_id=user.user_id).all()
            user_role_names = [role.role_name for role in user_roles]
            
            logger.info(f"User {user.user_id} has roles: {user_role_names}")
            logger.info(f"Required roles: {roles}")
            
            if not any(role in roles for role in user_role_names):
                logger.warning(f"Insufficient permissions: user roles {user_role_names} do not match required {roles}")
                return jsonify({"error": "Insufficient permissions"}), 403
            
            logger.info("User has required role, access granted")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
