from . import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class Ride(db.Model):
    __tablename__ = 'ride'
    
    ride_id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('driver.user_id'))
    starting_location = Column(String(255))  # Changed from JSON to String for location name
    dropoff_location = Column(String(255))  # Changed from JSON to String for location name
    request_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")  # pending, active, completed, cancelled
    passenger_count = Column(Integer, default=0)
    
    # Relationships
    driver = relationship("Driver", foreign_keys=[driver_id])
    passenger_rides = relationship("PassengerRide", backref="ride")
    feedback = relationship("Feedback", backref="ride")
    chats = relationship("Chat", backref="ride")

class PassengerRide(db.Model):
    __tablename__ = 'passenger_ride'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    ride_id = Column(Integer, ForeignKey('ride.ride_id'), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, rejected, completed
    
    # Create a composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'ride_id'),
    ) 