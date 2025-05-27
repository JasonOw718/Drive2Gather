from . import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Notification(db.Model):
    __tablename__ = 'notification'
    
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    message = Column(String(255), nullable=False)
    read = Column(Boolean, default=False)
    time = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with User is defined in User model 