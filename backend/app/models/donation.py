from . import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Donation(db.Model):
    __tablename__ = 'donation'
    
    donation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    donor_id = Column(Integer, ForeignKey('donor.user_id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String(255))
    payment_method = Column(String(50), default='stripe')
    
    # Relationship with User is defined in User model
    # Relationship with Donor is defined in Donor model 