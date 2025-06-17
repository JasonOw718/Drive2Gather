from flask import Blueprint, request, jsonify
from app.services import notification_service
from app.utils.jwt_handler import token_required, role_required

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('', methods=['GET'])
@token_required
def get_user_notifications():
    """Get all notifications for the authenticated user"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Get query parameters
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    
    # Validate pagination parameters
    if page < 1 or size < 1:
        return jsonify({"error": "Page and size must be positive integers"}), 400
    
    # Get user notifications
    notifications_data = notification_service.get_user_notifications(
        user_id=user_id,
        page=page,
        size=size,
        unread_only=unread_only
    )
    
    return jsonify(notifications_data), 200

@notification_bp.route('/read-all', methods=['PUT'])
@token_required
def mark_all_notifications_read():
    """Mark all notifications as read for the authenticated user"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id

    # Mark all notifications as read
    result, error = notification_service.mark_all_notifications_read(
        user_id=user_id
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "All notifications marked as read", "count": result}), 200 


@notification_bp.route('/read/<int:notification_id>', methods=['PUT'])
@token_required
def mark_notification_as_read(notification_id):
    """Mark a specific notification as read for the authenticated user"""
    user_id = request.user.user_id

    result, error = notification_service.mark_notification_read(
        user_id=user_id, notification_id=notification_id
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Notification marked as read", "notification_id": notification_id}), 200
