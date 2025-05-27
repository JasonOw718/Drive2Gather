from . import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Chat(db.Model):
    __tablename__ = 'chat'
    
    chat_id = Column(Integer, primary_key=True)
    ride_id = Column(Integer, ForeignKey('ride.ride_id'))
    
    # Relationships
    messages = relationship("Message", backref="chat")

class Message(db.Model):
    __tablename__ = 'message'
    
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.chat_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))
    content = Column(Text, nullable=False)
    send_time = Column(DateTime, default=datetime.utcnow)
    
    # Relationships are defined in User and Chat models 