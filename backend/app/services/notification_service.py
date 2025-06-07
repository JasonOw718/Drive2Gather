from datetime import datetime
from sqlalchemy import desc
from app.models import db, Notification, User
import logging

logger = logging.getLogger(__name__)

def create_notification(user_id, message):
    """
    Create a new notification for a user
    
    Args:
        user_id (int): ID of the user
        message (str): Notification message
        
    Returns:
        tuple: (notification, error)
    """
    try:
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return None, f"User with ID {user_id} not found"
            
        # Create new notification
        notification = Notification(
            user_id=user_id,
            message=message,
            read=False,
            time=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return notification, None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating notification: {str(e)}")
        return None, str(e)

def get_user_notifications(user_id, page=1, size=20, unread_only=False):
    """
    Get notifications for a specific user
    
    Args:
        user_id (int): ID of the user
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        unread_only (bool): Only return unread notifications if True
        
    Returns:
        dict: Dictionary containing notifications and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Create base query
    query = Notification.query.filter(Notification.user_id == user_id)
    
    # Filter by read status if unread_only is True
    if unread_only:
        query = query.filter(Notification.read == False)
    
    # Get total count
    total = query.count()
    
    # Get paginated notifications
    notifications = query.order_by(desc(Notification.time)).offset(offset).limit(size).all()
    
    # Format notifications
    formatted_notifications = []
    for notification in notifications:
        formatted_notifications.append({
            "id": notification.notification_id,
            "message": notification.message,
            "read": notification.read,
            "time": notification.time.isoformat()
        })
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Calculate pagination values
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "notifications": formatted_notifications,
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalNotifications": total,
            "nextPage": next_page,
            "prevPage": prev_page
        },
        "unreadCount": query.filter(Notification.read == False).count()
    }

def mark_notification_read(notification_id, user_id):
    """
    Mark a notification as read
    
    Args:
        notification_id (int): ID of the notification
        user_id (int): ID of the user
        
    Returns:
        tuple: (success, error)
    """
    try:
        # Get notification
        notification = Notification.query.get(notification_id)
        if not notification:
            return False, f"Notification with ID {notification_id} not found"
        
        # Check if notification belongs to user
        if notification.user_id != user_id:
            return False, "You do not have permission to access this notification"
        
        # Update notification
        notification.read = True
        db.session.commit()
        
        return True, None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking notification as read: {str(e)}")
        return False, str(e)

def mark_all_notifications_read(user_id):
    """
    Mark all notifications as read for a user
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        tuple: (count, error)
    """
    try:
        # Update all unread notifications for the user
        result = db.session.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.read == False
        ).update({Notification.read: True})
        
        db.session.commit()
        
        return result, None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error marking all notifications as read: {str(e)}")
        return 0, str(e)

# Helper functions for creating notifications for specific actions

def notify_ride_request(ride_id, driver_id, passenger_id, passenger_name, from_location, to_location):
    """Create a notification for a ride request"""
    message = f"New ride request from {passenger_name} for the trip from {from_location} to {to_location}"
    return create_notification(driver_id, message)

def notify_ride_request_approved(ride_id, driver_id, driver_name, passenger_id, from_location, to_location):
    """Create a notification for an approved ride request"""
    message = f"Your ride request from {from_location} to {to_location} has been approved by driver {driver_name}"
    return create_notification(passenger_id, message)

def notify_ride_request_rejected(ride_id, driver_id, driver_name, passenger_id, from_location, to_location):
    """Create a notification for a rejected ride request"""
    message = f"Your ride request from {from_location} to {to_location} has been rejected by driver {driver_name}"
    return create_notification(passenger_id, message)

def notify_ride_request_cancelled(ride_id, driver_id, passenger_id, passenger_name, from_location, to_location):
    """Create a notification for a cancelled ride request"""
    message = f"Ride request from {passenger_name} for the trip from {from_location} to {to_location} has been cancelled"
    return create_notification(driver_id, message)

def notify_ride_published(driver_id, driver_name, from_location, to_location):
    """Create a notification for a published ride"""
    message = f"Your ride from {from_location} to {to_location} has been published successfully"
    return create_notification(driver_id, message)

def notify_ride_request_submitted(passenger_id, from_location, to_location):
    """Create a notification for a passenger who submitted a ride request"""
    message = f"You have submitted a ride request from {from_location} to {to_location}"
    return create_notification(passenger_id, message)

def notify_ride_request_cancelled_passenger(passenger_id, from_location, to_location):
    """Create a notification for a passenger who cancelled their ride request"""
    message = f"You have cancelled your ride request from {from_location} to {to_location}"
    return create_notification(passenger_id, message) 