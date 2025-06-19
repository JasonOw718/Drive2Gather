from flask import Blueprint, request, jsonify, make_response
from app.services import feedback_service
from app.utils.jwt_handler import token_required, decode_token
from app.models import UserRole

# Create a blueprint for feedback routes
feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])
def submit_feedback():
    """Submit feedback/report about a ride"""
    # Check if the request is form data or JSON
    if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
        ride_id = request.form.get('ride_id')
        issue_type = request.form.get('issue_type')
        comments = request.form.get('comments', '')
        token = request.form.get('token')
    else:
        # Handle JSON data as before
        data = request.json or {}
        ride_id = data.get('ride_id')
        issue_type = data.get('issue_type')
        comments = data.get('comments', '')
        token = data.get('token')
    
    # Validate required fields
    if not all([ride_id, issue_type, token]):
        return jsonify({"error": "Missing required fields: ride_id, issue_type, and token are required"}), 400
    
    # Convert ride_id to integer
    try:
        ride_id = int(ride_id)
    except (ValueError, TypeError):
        return jsonify({"error": "ride_id must be a valid integer"}), 400
    
    # Authenticate using token from request body instead of header
    payload, error = decode_token(token)
    if error:
        return jsonify({"error": "Authentication failed: " + error}), 401
        
    try:
        user_id = int(payload['sub'])
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid token format"}), 401
    
    # Create feedback
    feedback_id, error = feedback_service.create_feedback(
        user_id=user_id,
        ride_id=ride_id,
        issue_type=issue_type,
        comments=comments
    )
    
    if error:
        return jsonify({"error": error}), 500
    
    # Set CORS headers for all responses
    response = jsonify({
        "message": "Feedback submitted successfully",
        "feedback_id": feedback_id
    })
    return response, 200

@feedback_bp.route('/admin/feedbacks', methods=['GET'])
@token_required
def get_all_feedbacks(current_user):
    """Get all feedback reports (admin only)"""
    # Check if user has admin role
    admin_role = UserRole.query.filter_by(user_id=current_user.user_id, role_name='admin').first()
    
    if not admin_role:
        return jsonify({"error": "Unauthorized: Admin access required"}), 403
    
    feedback_list, error = feedback_service.get_all_feedback()
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({
        "feedbacks": feedback_list
    }), 200 