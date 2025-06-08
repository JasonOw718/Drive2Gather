import logging
from app.models import User, Driver, UserRole, db
from math import ceil

# Configure logging
logger = logging.getLogger('admin_service')

def get_all_drivers(page=1, per_page=10, status=None):
    """
    Get all drivers with basic information with pagination
    
    Args:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        status (str, optional): Filter by verification status (pending, approved, rejected)
        
    Returns:
        tuple: (drivers_list, total_pages, total_drivers, error)
    """
    try:
        # Query users who have a driver profile
        query = db.session.query(
            User.name,
            User.email,
            User.phone,
            User.user_id,
            Driver.license_number,
            Driver.car_number,
            Driver.car_type,
            Driver.car_color,
            Driver.verification_status
        ).join(
            Driver, User.user_id == Driver.user_id
        )
        
        # Apply status filter if provided
        if status:
            query = query.filter(Driver.verification_status == status)
        
        # Count total drivers for pagination
        total_drivers = query.count()
        total_pages = ceil(total_drivers / per_page) if total_drivers > 0 else 1
        
        # Apply pagination
        drivers = query.order_by(User.user_id).offset((page - 1) * per_page).limit(per_page).all()
        
        # Format driver data
        drivers_list = []
        for driver_info in drivers:
            drivers_list.append({
                "id": driver_info[3],
                "name": driver_info[0],
                "email": driver_info[1],
                "phone": driver_info[2],
                "license_number": driver_info[4],
                "car_number": driver_info[5],
                "car_type": driver_info[6],
                "car_color": driver_info[7],
                "verification_status": driver_info[8]
            })
        
        return drivers_list, total_pages, total_drivers, None
    except Exception as e:
        logger.error(f"Error fetching drivers: {str(e)}")
        return None, 0, 0, str(e)

def get_all_users(page=1, per_page=10, role=None):
    """
    Get all users with pagination
    
    Args:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10)
        role (str, optional): Filter by role (passenger, driver, admin)
        
    Returns:
        tuple: (users_list, total_pages, total_users, error)
    """
    try:
        # Query for users with their roles
        query = db.session.query(
            User.user_id,
            User.name,
            User.email,
            User.phone,
            UserRole.role_name
        ).join(
            UserRole, User.user_id == UserRole.user_id, isouter=True
        )
        
        # Apply role filter if provided
        if role:
            query = query.filter(UserRole.role_name == role)
        # Filter out admin users when no specific role is requested
        elif role is None:
            query = query.filter(UserRole.role_name != 'admin')
        
        # Count total users for pagination
        total_users = query.count()
        total_pages = ceil(total_users / per_page) if total_users > 0 else 1
        
        # Apply pagination
        users = query.order_by(User.user_id).offset((page - 1) * per_page).limit(per_page).all()
        
        # Format user data
        users_list = []
        for user_info in users:
            users_list.append({
                "id": user_info[0],
                "name": user_info[1],
                "email": user_info[2],
                "phone": user_info[3],
                "role": user_info[4] or "passenger"  # Default to passenger if no role found
            })
        
        return users_list, total_pages, total_users, None
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return None, 0, 0, str(e)

def delete_user(user_id):
    """
    Delete a user by ID with cascade deletion of all associated records
    
    Args:
        user_id (int): ID of the user to delete
        
    Returns:
        tuple: (success, error)
    """
    try:
        # Disable autoflush to prevent premature constraint checks
        with db.session.no_autoflush:
            # Begin transaction
            user = User.query.get(user_id)
            if not user:
                return False, f"User with ID {user_id} not found"
            
            logger.info(f"Starting cascade deletion for user ID {user_id}")
            
            # Delete donations related to the user (both as donor and recipient)
            from app.models import Donation
            donor_donations = Donation.query.filter_by(donor_id=user_id).all()
            recipient_donations = Donation.query.filter_by(user_id=user_id).all()
            
            for donation in donor_donations + recipient_donations:
                logger.info(f"Deleting donation ID {donation.donation_id}")
                db.session.delete(donation)
            
            # Delete ride related data
            from app.models import Ride, PassengerRide
            
            # Delete passenger ride relations
            passenger_rides = PassengerRide.query.filter_by(user_id=user_id).all()
            for p_ride in passenger_rides:
                logger.info(f"Deleting passenger ride for user {p_ride.user_id} and ride {p_ride.ride_id}")
                db.session.delete(p_ride)
            
            # Get all rides where user is the driver
            driver_rides = Ride.query.filter_by(driver_id=user_id).all()
            ride_ids = [ride.ride_id for ride in driver_rides]
            
            # Delete all feedback related to the user's rides first
            from app.models import Feedback
            if ride_ids:
                Feedback.query.filter(Feedback.ride_id.in_(ride_ids)).delete(synchronize_session=False)
                logger.info(f"Deleted feedback for ride IDs: {ride_ids}")
                
            # Delete feedback submitted by the user
            Feedback.query.filter_by(user_id=user_id).delete(synchronize_session=False)
            logger.info(f"Deleted feedback submitted by user ID {user_id}")
            
            # Now delete the rides where user is the driver
            for ride in driver_rides:
                # First delete any passenger relationships for this ride
                PassengerRide.query.filter_by(ride_id=ride.ride_id).delete(synchronize_session=False)
                logger.info(f"Deleting ride ID {ride.ride_id}")
                db.session.delete(ride)
            
            # Delete notifications
            from app.models import Notification
            notifications = Notification.query.filter_by(user_id=user_id).all()
            for notification in notifications:
                logger.info(f"Deleting notification ID {notification.notification_id}")
                db.session.delete(notification)
                
            # Delete chat messages
            from app.models import Message, Chat
            
            # First get all chats associated with user's rides (as driver)
            driver_chat_ids = db.session.query(Chat.chat_id).join(Ride, Chat.ride_id == Ride.ride_id).filter(Ride.driver_id == user_id).all()
            driver_chat_ids = [chat_id[0] for chat_id in driver_chat_ids]
            
            # Get messages sent by this user
            messages = Message.query.filter(
                (Message.user_id == user_id) | 
                (Message.chat_id.in_(driver_chat_ids) if driver_chat_ids else False)
            ).all()
            
            for message in messages:
                logger.info(f"Deleting message ID {message.message_id}")
                db.session.delete(message)
                
            # Delete chats where the user's rides (as driver) were involved
            for chat_id in driver_chat_ids:
                logger.info(f"Deleting chat ID {chat_id}")
                Chat.query.filter_by(chat_id=chat_id).delete()
            
            # Delete user roles
            UserRole.query.filter_by(user_id=user_id).delete()
            logger.info(f"Deleted user roles for user ID {user_id}")
            
            # Delete donor profile if exists
            from app.models import Donor
            Donor.query.filter_by(user_id=user_id).delete()
            logger.info(f"Deleted donor profile for user ID {user_id}")
            
            # Delete driver profile if exists
            Driver.query.filter_by(user_id=user_id).delete()
            logger.info(f"Deleted driver profile for user ID {user_id}")
            
            # Delete passenger profile if exists
            from app.models import Passenger
            Passenger.query.filter_by(user_id=user_id).delete()
            logger.info(f"Deleted passenger profile for user ID {user_id}")
            
            # Finally delete the user
            db.session.delete(user)
            logger.info(f"Deleted user ID {user_id}")
            
        # Commit all changes after the no_autoflush block
        db.session.commit()
        logger.info(f"Successfully completed cascade deletion for user ID {user_id}")
        
        return True, None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user: {str(e)}")
        return False, str(e)

def update_driver_verification_status(driver_id, status):
    """
    Update a driver's verification status
    
    Args:
        driver_id (int): ID of the driver
        status (str): New status (approved, rejected)
        
    Returns:
        tuple: (success, error)
    """
    try:
        driver = Driver.query.filter_by(user_id=driver_id).first()
        if not driver:
            return False, f"Driver with ID {driver_id} not found"
        
        # Update status
        driver.verification_status = status
        db.session.commit()
        
        return True, None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating driver status: {str(e)}")
        return False, str(e) 