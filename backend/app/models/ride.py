from . import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from datetime import datetime

class Ride(db.Model):
    __tablename__ = 'ride'
    
    ride_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    driver_id = Column(Integer, ForeignKey('driver.user_id'))
    starting_location = Column(JSON)  # Using JSON type for point data
    dropoff_location = Column(JSON)  # Using JSON type for point data
    request_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")  # pending, active, completed, cancelled
    passenger_count = Column(Integer, default=0)
    fare = Column(Float)
    
    # Relationships
    driver = relationship("Driver", foreign_keys=[driver_id])
    passenger_rides = relationship("PassengerRide", backref="ride")
    feedback = relationship("Feedback", backref="ride")
    chats = relationship("Chat", backref="ride")

class PassengerRide(db.Model):
    __tablename__ = 'passenger_ride'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    ride_id = Column(Integer, ForeignKey('ride.ride_id'), nullable=False) 