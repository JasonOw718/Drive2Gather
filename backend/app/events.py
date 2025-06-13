from flask_socketio import emit, join_room, leave_room
from app import socketio

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected'})

@socketio.on('join')
def handle_join(data):
    """Handle client joining a chat room"""
    chat_id = data.get('chat_id')
    if chat_id:
        room = f'chat_{chat_id}'
        join_room(room)
        emit('joined', {'chat_id': chat_id}, room=room)

@socketio.on('leave')
def handle_leave(data):
    """Handle client leaving a chat room"""
    chat_id = data.get('chat_id')
    if chat_id:
        room = f'chat_{chat_id}'
        leave_room(room)
        emit('left', {'chat_id': chat_id}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    pass  # Add any cleanup if needed 