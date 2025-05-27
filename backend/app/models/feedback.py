from . import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    ride_id = Column(Integer, ForeignKey('ride.ride_id'), nullable=False)
    rating = Column(Integer)  # 1-5 star rating
    comments = Column(Text)
    comment_time = Column(DateTime, default=datetime.utcnow)
    
    # Relationships are handled in User and Ride models 