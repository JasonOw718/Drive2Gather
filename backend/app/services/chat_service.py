from app.models import db
from app.models.message import Chat, Message
from app.models.ride import Ride
from app.models.user import User
from datetime import datetime
from app import socketio

def create_chat_for_ride(ride_id):
    """
    Create a new chat for a ride
    
    Args:
        ride_id (int): The ID of the ride to create a chat for
        
    Returns:
        tuple: (chat_data, error)
            - chat_data: Dictionary containing chat information if successful
            - error: Error message if unsuccessful, None otherwise
    """
    # Check if ride exists
    ride = Ride.query.get(ride_id)
    if not ride:
        return None, "Ride not found"
    
    # Check if chat already exists for this ride
    existing_chat = Chat.query.filter_by(ride_id=ride_id).first()
    if existing_chat:
        return {
            'chat_id': existing_chat.chat_id,
            'ride_id': existing_chat.ride_id
        }, None
    
    # Create new chat
    try:
        new_chat = Chat(ride_id=ride_id)
        db.session.add(new_chat)
        db.session.commit()
        
        return {
            'chat_id': new_chat.chat_id,
            'ride_id': new_chat.ride_id
        }, None
    except Exception as e:
        db.session.rollback()
        return None, f"Error creating chat: {str(e)}"

def get_chat_by_ride_id(ride_id):
    """
    Get a chat by ride ID, create one if it doesn't exist
    
    Args:
        ride_id (int): The ID of the ride
        
    Returns:
        tuple: (chat_data, error)
            - chat_data: Dictionary containing chat information if successful
            - error: Error message if unsuccessful, None otherwise
    """
    # Check if ride exists
    ride = Ride.query.get(ride_id)
    if not ride:
        return None, "Ride not found"
    
    # Get chat for this ride
    chat = Chat.query.filter_by(ride_id=ride_id).first()
    if not chat:
        # Create a new chat if it doesn't exist
        return create_chat_for_ride(ride_id)
    
    return {
        'chat_id': chat.chat_id,
        'ride_id': chat.ride_id
    }, None

def get_messages(chat_id):
    """
    Get all messages for a chat
    
    Args:
        chat_id (int): The ID of the chat
        
    Returns:
        tuple: (messages_data, error)
            - messages_data: List of messages if successful
            - error: Error message if unsuccessful, None otherwise
    """
    # Check if chat exists
    chat = Chat.query.get(chat_id)
    if not chat:
        return None, "Chat not found"
    
    # Get all messages for this chat
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.send_time).all()
    
    # Format messages
    messages_list = []
    for message in messages:
        user = User.query.get(message.user_id)
        messages_list.append({
            'message_id': message.message_id,
            'user_id': message.user_id,
            'username': user.name if user else 'Unknown',
            'content': message.content,
            'send_time': message.send_time.isoformat()
        })
    
    return {
        'chat_id': chat_id,
        'messages': messages_list
    }, None

def send_message(chat_id, user_id, content):
    """
    Send a message in a chat
    
    Args:
        chat_id (int): The ID of the chat
        user_id (int): The ID of the user sending the message
        content (str): The message content
        
    Returns:
        tuple: (message_data, error)
            - message_data: Dictionary containing message information if successful
            - error: Error message if unsuccessful, None otherwise
    """
    # Check if chat exists
    chat = Chat.query.get(chat_id)
    if not chat:
        return None, "Chat not found"
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return None, "User not found"
    
    # Create new message
    try:
        new_message = Message(
            chat_id=chat_id,
            user_id=user_id,
            content=content,
            send_time=datetime.utcnow()
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        # Format message data
        message_data = {
            'message_id': new_message.message_id,
            'user_id': user_id,
            'username': user.name,
            'content': new_message.content,
            'send_time': new_message.send_time.isoformat()
        }
        
        # Emit the new message to all clients in the chat room
        socketio.emit('new_message', {
            'chat_id': chat_id,
            'message': message_data
        }, room=f'chat_{chat_id}')
        
        return message_data, None
    except Exception as e:
        db.session.rollback()
        return None, f"Error sending message: {str(e)}"

def get_user_chats(user_id):
    """
    Get all chats for a user (rides where user is driver or passenger)
    
    Args:
        user_id (int): The ID of the user
        
    Returns:
        tuple: (chats_data, error)
            - chats_data: List of chats if successful
            - error: Error message if unsuccessful, None otherwise
    """
    from app.models.ride import Ride, PassengerRide
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return None, "User not found"
    
    try:
        # Get rides where user is driver
        driver_rides = Ride.query.filter_by(driver_id=user_id).all()
        
        # Get rides where user is passenger
        passenger_rides = db.session.query(Ride).join(
            PassengerRide, Ride.ride_id == PassengerRide.ride_id
        ).filter(PassengerRide.user_id == user_id).all()
        
        # Combine and deduplicate rides
        all_rides = list(set(driver_rides + passenger_rides))
        
        # Get chats for these rides
        chats = []
        for ride in all_rides:
            chat = Chat.query.filter_by(ride_id=ride.ride_id).first()
            if chat:
                # Get last message
                last_message = Message.query.filter_by(chat_id=chat.chat_id).order_by(Message.send_time.desc()).first()
                
                chats.append({
                    'chat_id': chat.chat_id,
                    'ride_id': ride.ride_id,
                    'starting_location': ride.starting_location,
                    'dropoff_location': ride.dropoff_location,
                    'last_message': {
                        'content': last_message.content if last_message else None,
                        'send_time': last_message.send_time.isoformat() if last_message else None
                    }
                })
        
        return {'chats': chats}, None
    except Exception as e:
        return None, f"Error getting user chats: {str(e)}" 