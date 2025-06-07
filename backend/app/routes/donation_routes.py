from flask import Blueprint, request, jsonify
from app.services import donation_service, notification_service
from app.utils.jwt_handler import token_required, role_required
from app.models import User, db
import logging

donation_bp = Blueprint('donations', __name__)

@donation_bp.route('', methods=['POST'])
@token_required
def create_donation():
    """Create a new donation"""
    try:
        # Get request data
        data = request.json
        
        # Validate required fields
        required_fields = ['userId', 'donorId', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return jsonify({"error": "Amount must be greater than 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid amount format"}), 400
        
        # Get the current user ID (should match donorId for security)
        current_user_id = request.user.user_id
        
        # Ensure the donor ID matches the current user
        if int(data['donorId']) != current_user_id:
            return jsonify({"error": "Donor ID must match authenticated user"}), 403
        
        # Get payment method (default to stripe if not provided)
        payment_method = data.get('paymentMethod', 'stripe')
        
        # Validate payment method
        if payment_method not in ['stripe', 'paypal']:
            return jsonify({"error": "Invalid payment method. Must be 'stripe' or 'paypal'"}), 400
        
        # Create donation
        donation_data, error = donation_service.create_donation(
            user_id=data['userId'],
            donor_id=data['donorId'],
            amount=amount,
            payment_method=payment_method,
            description=data.get('description')
        )
        
        if error:
            return jsonify({"error": error}), 400
        
        # Get recipient and donor info for notification
        recipient = User.query.get(data['userId'])
        donor = User.query.get(data['donorId'])
        
        if recipient and donor:
            # Create notification for the recipient
            notification_service.create_notification(
                user_id=data['userId'],
                message=f"You received a donation of RM {amount:.2f} from {donor.name} via {payment_method.capitalize()}."
            )
        
        return jsonify(donation_data), 201
    except Exception as e:
        logging.exception(f"Unexpected error in create_donation: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@donation_bp.route('/received', methods=['GET'])
@token_required
def get_received_donations():
    """Get donations received by the authenticated user"""
    try:
        # Get pagination parameters
        try:
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 20))
        except ValueError:
            return jsonify({"error": "Invalid pagination parameters"}), 400
        
        # Validate pagination parameters
        if page < 1 or size < 1:
            return jsonify({"error": "Page and size must be positive integers"}), 400
        
        # Get user ID from authenticated user
        user_id = request.user.user_id
        
        # Get donations
        donations_data = donation_service.get_user_donations(
            user_id=user_id,
            page=page,
            size=size
        )
        
        return jsonify(donations_data), 200
    except Exception as e:
        logging.exception(f"Unexpected error in get_received_donations: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@donation_bp.route('/made', methods=['GET'])
@token_required
def get_made_donations():
    """Get donations made by the authenticated user"""
    try:
        # Get pagination parameters
        try:
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 20))
        except ValueError:
            return jsonify({"error": "Invalid pagination parameters"}), 400
        
        # Validate pagination parameters
        if page < 1 or size < 1:
            return jsonify({"error": "Page and size must be positive integers"}), 400
        
        # Get user ID from authenticated user
        user_id = request.user.user_id
        
        # Get donations
        donations_data = donation_service.get_donor_donations(
            donor_id=user_id,
            page=page,
            size=size
        )
        
        return jsonify(donations_data), 200
    except Exception as e:
        logging.exception(f"Unexpected error in get_made_donations: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500 