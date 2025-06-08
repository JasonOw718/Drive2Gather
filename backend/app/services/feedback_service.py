import logging
from app.models import db, Feedback, User, Ride
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logger = logging.getLogger('feedback_service')

def create_feedback(user_id, ride_id, issue_type, comments):
    """
    Create a new feedback record
    
    Args:
        user_id (int): User ID who submitted the feedback
        ride_id (int): Ride ID the feedback is about
        issue_type (str): Type of issue reported
        comments (str): Additional comments or description
        
    Returns:
        tuple: (feedback_id, error)
    """
    try:
        # Create new feedback
        new_feedback = Feedback(
            user_id=user_id,
            ride_id=ride_id,
            issue_type=issue_type,
            comments=comments
        )
        
        # Add and commit to database
        db.session.add(new_feedback)
        db.session.commit()
        
        return new_feedback.feedback_id, None
    except SQLAlchemyError as e:
        db.session.rollback()
        error_message = f"Error creating feedback: {str(e)}"
        logger.error(error_message)
        return None, error_message

def get_all_feedback():
    """
    Get all feedback reports
    
    Returns:
        tuple: (feedback_list, error)
    """
    try:
        # Query for all feedback entries with related user (passenger) and ride information
        feedback_query = db.session.query(
            Feedback,
            User.name.label('passenger_name'),
            Ride.driver_id
        ).join(
            User, Feedback.user_id == User.user_id
        ).join(
            Ride, Feedback.ride_id == Ride.ride_id
        ).all()
        
        # Format feedback data
        feedback_list = []
        for result in feedback_query:
            feedback = result[0]
            passenger_name = result[1]
            driver_id = result[2]
            
            # Get driver name
            driver = User.query.get(driver_id)
            driver_name = driver.name if driver else f"Unknown Driver (ID: {driver_id})"
            
            feedback_list.append({
                "feedback_id": feedback.feedback_id,
                "user_id": feedback.user_id,
                "passenger_name": passenger_name,
                "ride_id": feedback.ride_id,
                "driver_id": driver_id,
                "driver_name": driver_name,
                "issue_type": feedback.issue_type,
                "comments": feedback.comments,
                "comment_time": feedback.comment_time.isoformat() if feedback.comment_time else None
            })
        
        return feedback_list, None
    except SQLAlchemyError as e:
        error_message = f"Error fetching feedback: {str(e)}"
        logger.error(error_message)
        return None, error_message 