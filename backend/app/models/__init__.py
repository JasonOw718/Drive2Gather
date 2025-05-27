from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, UserRole, Admin, Donor, Passenger, Driver
from .notification import Notification
from .ride import Ride, PassengerRide
from .donation import Donation
from .feedback import Feedback
from .message import Message, Chat
