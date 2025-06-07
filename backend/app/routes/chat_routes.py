from flask import Blueprint, request, jsonify, g
from app.models import db
from app.utils.jwt_handler import token_required
from app.services import chat_service
from datetime import datetime

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chats')

@chat_bp.route('/ride/<int:ride_id>', methods=['GET'])
@token_required
def get_chat_by_ride(ride_id):
    """Get chat by ride ID"""
    chat_data, error = chat_service.get_chat_by_ride_id(ride_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(chat_data), 200

@chat_bp.route('/<int:chat_id>/messages', methods=['GET'])
@token_required
def get_messages(chat_id):
    """Get all messages for a chat"""
    messages_data, error = chat_service.get_messages(chat_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(messages_data), 200

@chat_bp.route('/<int:chat_id>/messages', methods=['POST'])
@token_required
def send_message(chat_id):
    """Send a message in a chat"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    # Get user ID from token
    try:
        user_id = request.user.user_id
    except AttributeError:
        # If g.user is not set correctly, try to get it from the token
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header:
            return jsonify({'error': 'Authentication required'}), 401
            
        token = auth_header.split('Bearer ')[1]
        from app.utils.jwt_handler import decode_token
        payload, error = decode_token(token)
        
        if error:
            return jsonify({'error': error}), 401
            
        try:
            user_id = int(payload['sub'])
        except (ValueError, KeyError):
            return jsonify({'error': 'Invalid token format'}), 401
    
    message_data, error = chat_service.send_message(
        chat_id=chat_id,
        user_id=user_id,
        content=data['content']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(message_data), 201

@chat_bp.route('/user/<int:user_id>/chats', methods=['GET'])
@token_required
def get_user_chats(user_id):
    """Get all chats for a user (rides where user is driver or passenger)"""
    chats_data, error = chat_service.get_user_chats(user_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(chats_data), 200 