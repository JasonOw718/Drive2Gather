from . import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    password = Column(String(255), nullable=False)
    
    # Relationships
    roles = relationship("UserRole", backref="user")
    notifications = relationship("Notification", backref="user")
    messages = relationship("Message", backref="user")
    passenger_rides = relationship("PassengerRide", backref="user")
    donations = relationship("Donation", foreign_keys="Donation.user_id", backref="user")

class UserRole(db.Model):
    __tablename__ = 'user_role'
    
    role_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    role_name = Column(String(50), nullable=False)

    def __init__(self, role_name):
        self.role_name = role_name

class Admin(db.Model):
    __tablename__ = 'admin'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    
    user = relationship("User", backref="admin_profile")

class Donor(db.Model):
    __tablename__ = 'donor'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    
    user = relationship("User", backref="donor_profile")
    donations = relationship("Donation", foreign_keys="Donation.donor_id", backref="donor")

class Passenger(db.Model):
    __tablename__ = 'passenger'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    
    user = relationship("User", backref="passenger_profile")

class Driver(db.Model):
    __tablename__ = 'driver'
    
    user_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    license_number = Column(String(50))
    car_number = Column(String(20))
    car_type = Column(String(50))
    car_color = Column(String(30))
    
    user = relationship("User", backref="driver_profile")
    rides = relationship("Ride", backref="driver_user", foreign_keys="Ride.driver_id")
