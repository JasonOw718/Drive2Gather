import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # Initialize with default settings
            cls._instance.settings = {
                'DEBUG': os.environ.get('DEBUG', 'True').lower() == 'true',
                'TESTING': False,
                'SECRET_KEY': os.environ.get('SECRET_KEY', 'dev-key-for-development-only'),
                'SQLALCHEMY_TRACK_MODIFICATIONS': False,
                'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URI', 'sqlite:///drive2gather.sqlite'),
                
                # Mail configuration
                'MAIL_SERVER': os.environ.get('MAIL_SERVER', 'smtp.example.com'),
                'MAIL_PORT': int(os.environ.get('MAIL_PORT', 587)),
                'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
                'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', 'noreply@drive2gather.com'),
                'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', 'password'),
                'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@drive2gather.com')
            }
                
        return cls._instance
    
    def set_config(self, key, value):
        """Set a configuration value"""
        self.settings[key] = value
        
    def get_config(self, key):
        """Get a configuration value"""
        return self.settings.get(key, None)
