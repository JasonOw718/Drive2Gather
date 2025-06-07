from app.models import User, UserRole, Driver, Passenger, Ride, PassengerRide, db
from werkzeug.security import generate_password_hash
from datetime import datetime

# Base Entity class
class Entity:
    def __init__(self):
        self.data = {}
    
    def get_data(self):
        return self.data

# User Entity
class UserEntity(Entity):
    def __init__(self):
        super().__init__()
        self.user = None
        
    def set_name(self, name):
        self.data['name'] = name
        return self
        
    def set_email(self, email):
        self.data['email'] = email
        return self
        
    def set_phone(self, phone):
        self.data['phone'] = phone
        return self
        
    def set_password(self, password):
        self.data['password'] = password
        return self
        
    def set_role(self, role):
        self.data['role'] = role
        return self
        
    def set_user_id(self, user_id):
        self.data['user_id'] = user_id
        return self

# Ride Entity
class RideEntity(Entity):
    def __init__(self):
        super().__init__()
        self.ride = None
        
    def set_driver_id(self, driver_id):
        self.data['driver_id'] = driver_id
        return self
        
    def set_starting_location(self, starting_location):
        self.data['starting_location'] = starting_location
        return self
        
    def set_dropoff_location(self, dropoff_location):
        self.data['dropoff_location'] = dropoff_location
        return self
        
    def set_request_time(self, request_time):
        self.data['request_time'] = request_time
        return self
        
    def set_status(self, status):
        self.data['status'] = status
        return self
        
    def set_passenger_count(self, passenger_count):
        self.data['passenger_count'] = passenger_count
        return self
        
    def set_ride_id(self, ride_id):
        self.data['ride_id'] = ride_id
        return self

# PassengerRide Entity
class PassengerRideEntity(Entity):
    def __init__(self):
        super().__init__()
        self.passenger_ride = None
        
    def set_user_id(self, user_id):
        self.data['user_id'] = user_id
        return self
        
    def set_ride_id(self, ride_id):
        self.data['ride_id'] = ride_id
        return self
        
    def set_status(self, status):
        self.data['status'] = status
        return self

# Builder Interface
class Builder:
    def build(self):
        pass

# User Builder
class UserBuilder(Builder):
    def __init__(self):
        self.user_entity = UserEntity()
        
    def set_name(self, name):
        self.user_entity.set_name(name)
        return self
        
    def set_email(self, email):
        self.user_entity.set_email(email)
        return self
        
    def set_phone(self, phone):
        self.user_entity.set_phone(phone)
        return self
        
    def set_password(self, password):
        self.user_entity.set_password(password)
        return self
        
    def set_role(self, role):
        self.user_entity.set_role(role)
        return self
        
    def set_user_id(self, user_id):
        self.user_entity.set_user_id(user_id)
        return self
        
    def build(self):
        data = self.user_entity.get_data()
        
        # Create a new user
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            password=generate_password_hash(data.get('password')) if data.get('password') else None
        )
        
        if data.get('user_id'):
            user.user_id = data.get('user_id')
            
        self.user_entity.user = user
        return user

# Driver Builder (extends UserBuilder)
class DriverBuilder(UserBuilder):
    def __init__(self):
        super().__init__()
        self.license_number = None
        self.car_number = None
        self.car_type = None
        self.car_color = None
        
    def set_license_number(self, license_number):
        self.license_number = license_number
        return self
        
    def set_car_number(self, car_number):
        self.car_number = car_number
        return self
        
    def set_car_type(self, car_type):
        self.car_type = car_type
        return self
        
    def set_car_color(self, car_color):
        self.car_color = car_color
        return self
        
    def build(self):
        # First build the user
        data = self.user_entity.get_data()
        
        # Create a new user directly instead of using super().build()
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            password=generate_password_hash(data.get('password')) if data.get('password') else None
        )
        
        # Create the driver with the same user_id
        driver = Driver(
            license_number=self.license_number,
            car_number=self.car_number,
            car_type=self.car_type,
            car_color=self.car_color
        )
        
        # We need to link the driver to the user
        driver.user = user
        
        return user, driver

# Ride Builder
class RideBuilder(Builder):
    def __init__(self):
        self.ride_entity = RideEntity()
        
    def set_driver_id(self, driver_id):
        self.ride_entity.set_driver_id(driver_id)
        return self
        
    def set_starting_location(self, starting_location):
        self.ride_entity.set_starting_location(starting_location)
        return self
        
    def set_dropoff_location(self, dropoff_location):
        self.ride_entity.set_dropoff_location(dropoff_location)
        return self
        
    def set_request_time(self, request_time):
        self.ride_entity.set_request_time(request_time)
        return self
        
    def set_status(self, status):
        self.ride_entity.set_status(status)
        return self
        
    def set_passenger_count(self, passenger_count):
        self.ride_entity.set_passenger_count(passenger_count)
        return self
        
    def build(self):
        data = self.ride_entity.get_data()
        
        # Use current time if not provided
        if 'request_time' not in data or data['request_time'] is None:
            data['request_time'] = datetime.utcnow()
            
        # Set default status if not provided
        if 'status' not in data or data['status'] is None:
            data['status'] = "pending"
        
        ride = Ride(
            driver_id=data.get('driver_id'),
            starting_location=data.get('starting_location'),
            dropoff_location=data.get('dropoff_location'),
            request_time=data.get('request_time'),
            status=data.get('status'),
            passenger_count=data.get('passenger_count', 0)
        )
        
        self.ride_entity.ride = ride
        return ride

# PassengerRide Builder
class PassengerRideBuilder(Builder):
    def __init__(self):
        self.passenger_ride_entity = PassengerRideEntity()
        
    def set_user_id(self, user_id):
        self.passenger_ride_entity.set_user_id(user_id)
        return self
        
    def set_ride_id(self, ride_id):
        self.passenger_ride_entity.set_ride_id(ride_id)
        return self
        
    def set_status(self, status):
        self.passenger_ride_entity.set_status(status)
        return self
        
    def build(self):
        data = self.passenger_ride_entity.get_data()
        
        # Set default status if not provided
        if 'status' not in data or data['status'] is None:
            data['status'] = "pending"
        
        passenger_ride = PassengerRide(
            user_id=data.get('user_id'),
            ride_id=data.get('ride_id'),
            status=data.get('status')
        )
        
        self.passenger_ride_entity.passenger_ride = passenger_ride
        return passenger_ride

# Director class
class Director:
    def __init__(self, builder):
        self.builder = builder
        
    def construct_user(self, data):
        if isinstance(self.builder, UserBuilder):
            self.builder.set_name(data.get('name'))
            self.builder.set_email(data.get('email'))
            
            if 'phone' in data:
                self.builder.set_phone(data.get('phone'))
                
            if 'password' in data:
                self.builder.set_password(data.get('password'))
                
            if 'role' in data:
                self.builder.set_role(data.get('role'))
                
        return self.builder.build()
        
    def construct_driver(self, data):
        if isinstance(self.builder, DriverBuilder):
            # First set user data
            self.builder.set_name(data.get('name'))
            self.builder.set_email(data.get('email'))
            
            if 'phone' in data:
                self.builder.set_phone(data.get('phone'))
                
            if 'password' in data:
                self.builder.set_password(data.get('password'))
                
            # Then set driver-specific data
            self.builder.set_license_number(data.get('license_number'))
            self.builder.set_car_number(data.get('car_number'))
            self.builder.set_car_type(data.get('car_type'))
            self.builder.set_car_color(data.get('car_color'))
            
        return self.builder.build()
        
    def construct_ride(self, data):
        if isinstance(self.builder, RideBuilder):
            self.builder.set_driver_id(data.get('driver_id'))
            self.builder.set_starting_location(data.get('starting_location'))
            self.builder.set_dropoff_location(data.get('dropoff_location'))
            
            if 'request_time' in data:
                self.builder.set_request_time(data.get('request_time'))
                
            if 'status' in data:
                self.builder.set_status(data.get('status'))
                
            if 'passenger_count' in data:
                self.builder.set_passenger_count(data.get('passenger_count'))
                
        return self.builder.build()
        
    def construct_passenger_ride(self, data):
        if isinstance(self.builder, PassengerRideBuilder):
            self.builder.set_user_id(data.get('user_id'))
            self.builder.set_ride_id(data.get('ride_id'))
            
            if 'status' in data:
                self.builder.set_status(data.get('status'))
                
        return self.builder.build() 