from flask import Blueprint, jsonify, request
from app.services import admin_service

# Create a blueprint for admin routes
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    """Get all drivers with pagination, defaulting to pending status"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 'pending')  # Default to pending status
    
    drivers_list, total_pages, total_drivers, error = admin_service.get_all_drivers(page, per_page, status)
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({
        "drivers": drivers_list,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_drivers": total_drivers
        }
    }), 200

@admin_bp.route('/drivers/<int:driver_id>/status', methods=['PUT'])
def update_driver_status(driver_id):
    """Update a driver's verification status"""
    data = request.json
    
    # Validate required fields
    if 'status' not in data:
        return jsonify({"error": "Missing required field: status"}), 400
    
    # Valid status values
    valid_statuses = ['pending', 'approved', 'rejected']
    if data['status'] not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
    
    # Update driver status
    success, error = admin_service.update_driver_verification_status(driver_id, data['status'])
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": f"Driver status updated to {data['status']}"}), 200

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    role = request.args.get('role')
    
    users_list, total_pages, total_users, error = admin_service.get_all_users(page, per_page, role)
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({
        "users": users_list,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_users": total_users
        }
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    success, error = admin_service.delete_user(user_id)
    
    if error:
        return jsonify({"error": error}), 500 if "not found" not in error else 404
    
    return jsonify({
        "success": success,
        "message": f"User with ID {user_id} has been deleted"
    }), 200

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Get a user's details by ID for admin"""
    from app.services.auth_service import get_user_profile
    
    # Get user profile
    user_data, error = get_user_profile(user_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    # Add additional fields for admin view
    try:
        from app.models import db, PassengerRide, Feedback
        from sqlalchemy import func
        
        # Get ride count
        ride_count = db.session.query(func.count()).filter(
            PassengerRide.user_id == user_id
        ).scalar() or 0
        
        # Get report/feedback count
        report_count = db.session.query(func.count(Feedback.feedback_id)).filter(
            Feedback.user_id == user_id
        ).scalar() or 0
        
        # Add to user data
        user_data["total_rides"] = ride_count
        user_data["total_reports"] = report_count
        user_data["is_active"] = True  # Default to active for now
        user_data["created_at"] = "2024-01-01"  # Placeholder, should be from User model
        
    except Exception as e:
        # Error encountered but continue with available data
        pass
    
    return jsonify({"user": user_data}), 200 