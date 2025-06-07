from app.models import Ride, db, User, Driver, PassengerRide
from sqlalchemy import desc, and_
from app.utils.builders import RideBuilder, PassengerRideBuilder, Director
from datetime import datetime
        

def format_time_simple(dt):
    """Format datetime to simple time format (e.g., '05:00 PM')"""
    return dt.strftime("%I:%M %p").lstrip("0")

def get_all_rides(page=1, size=20):
    """
    Get all rides with pagination, excluding completed rides
    
    Args:
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing rides and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get total count (exclude completed rides)
    total = Ride.query.filter(Ride.status != "completed").count()
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Get rides and their drivers
    # Use left joins to ensure we get all rides even if driver or user information is missing
    rides_query = db.session.query(Ride, User.name.label('driver_name'))\
        .filter(Ride.status != "completed")\
        .outerjoin(Driver, Ride.driver_id == Driver.user_id)\
        .outerjoin(User, Driver.user_id == User.user_id)\
        .order_by(desc(Ride.request_time))\
        .offset(offset)\
        .limit(size)
    
    rides = rides_query.all()
    
    # Format rides
    formatted_rides = []
    for ride_info in rides:
        ride = ride_info[0]  # The Ride object
        driver_name = ride_info[1] or "Unknown Driver"  # The driver name, with default if None
        
        formatted_rides.append({
            "rideID": ride.ride_id,
            "driverID": ride.driver_id,
            "startingLocation": ride.starting_location,
            "dropoffLocation": ride.dropoff_location,
            "requestTime": ride.request_time.isoformat(),
            "status": ride.status,
            "Passenger_count": ride.passenger_count,
            "driverName": driver_name
        })
    
    # Calculate pagination values
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "rides": formatted_rides,
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalRides": total,
            "nextPage": next_page,
            "prevPage": prev_page
        }
    }

def get_driver_ride_requests(driver_id, page=1, size=20):
    """
    Get all pending ride requests for a specific driver
    
    Args:
        driver_id (int): ID of the driver
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing ride requests and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get the driver's rides
    driver_rides = Ride.query.filter_by(driver_id=driver_id).all()
    
    if not driver_rides:
        return {
            "rideRequests": [],
            "pagination": {
                "currentPage": page,
                "pageSize": size,
                "totalPages": 0,
                "totalRequests": 0,
                "nextPage": None,
                "prevPage": None
            }
        }
    
    # Get ride IDs
    ride_ids = [ride.ride_id for ride in driver_rides]
    
    # Get total count of pending requests for these rides
    total = PassengerRide.query.filter(
        PassengerRide.ride_id.in_(ride_ids),
        PassengerRide.status == "pending"
    ).count()
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Get pending ride requests for these rides
    requests_query = db.session.query(
        PassengerRide, 
        User.name.label('passenger_name'),
        Ride.starting_location,
        Ride.dropoff_location,
        Ride.request_time,
        Ride.ride_id
    ).filter(
        PassengerRide.ride_id.in_(ride_ids),
        PassengerRide.status == "pending"
    ).join(Ride, PassengerRide.ride_id == Ride.ride_id)\
     .join(User, PassengerRide.user_id == User.user_id)\
     .order_by(desc(Ride.request_time))\
     .offset(offset)\
     .limit(size)
    
    request_results = requests_query.all()
    
    # Format ride requests
    formatted_requests = []
    for request_info in request_results:
        passenger_ride = request_info[0]
        passenger_name = request_info[1]
        starting_location = request_info[2]
        dropoff_location = request_info[3]
        request_time = request_info[4]
        ride_id = request_info[5]
        
        formatted_requests.append({
            "rideID": ride_id,
            "passengerID": passenger_ride.user_id,
            "passengerName": passenger_name,
            "startingLocation": starting_location,
            "dropoffLocation": dropoff_location,
            "requestTime": format_time_simple(request_time),
            "status": passenger_ride.status
        })
    
    # Calculate pagination values
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "rideRequests": formatted_requests,
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalRequests": total,
            "nextPage": next_page,
            "prevPage": prev_page
        }
    }

def approve_ride_request(ride_id, passenger_id, driver_id):
    """
    Approve a passenger's ride request
    
    Args:
        ride_id (int): ID of the ride
        passenger_id (int): ID of the passenger
        driver_id (int): ID of the driver
        
    Returns:
        tuple: (approval_data, error)
    """
    try:
        # Verify ride exists and belongs to the driver
        ride = Ride.query.filter_by(ride_id=ride_id, driver_id=driver_id).first()
        if not ride:
            return None, f"Ride not found or does not belong to driver {driver_id}"
        
        # Verify passenger exists
        passenger = User.query.get(passenger_id)
        if not passenger:
            return None, f"Passenger with ID {passenger_id} not found"
        
        # Find the passenger ride request
        passenger_ride = PassengerRide.query.filter_by(
            ride_id=ride_id,
            user_id=passenger_id,
            status="pending"
        ).first()
        
        if not passenger_ride:
            return None, f"No pending ride request found for passenger {passenger_id} on ride {ride_id}"
        
        # Update the status to approved
        passenger_ride.status = "approved"
        db.session.commit()
        
        # Format response
        approval_data = {
            "rideID": ride_id,
            "passengerID": passenger_id,
            "status": "approved",
            "message": f"Ride request for passenger {passenger_id} has been approved"
        }
        
        return approval_data, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_ride_by_id(ride_id):
    """
    Get details of a specific ride by ID
    
    Args:
        ride_id (int): ID of the ride
        
    Returns:
        tuple: (ride_data, error)
    """
    try:
        # Get the ride first to ensure it exists
        ride = Ride.query.get(ride_id)
        if not ride:
            return None, f"Ride with ID {ride_id} not found"
        
        # Get driver information if available
        driver_info = db.session.query(
            User.name.label('driver_name'),
            Driver.car_number,
            Driver.car_type,
            Driver.car_color
        ).join(Driver, User.user_id == Driver.user_id)\
         .filter(Driver.user_id == ride.driver_id)\
         .first()
        
        # Set default values if driver info not found
        driver_name = driver_info[0] if driver_info else "Unknown Driver"
        car_number = driver_info[1] if driver_info else "Unknown"
        car_type = driver_info[2] if driver_info else "Unknown"
        car_color = driver_info[3] if driver_info else "Unknown"
        
        # Format response
        ride_data = {
            "rideDetails": {
                "requestTime": format_time_simple(ride.request_time),
                "startingLocation": ride.starting_location,
                "dropoffLocation": ride.dropoff_location,
                "Passenger_count": ride.passenger_count,
                "driverInfo": {
                    "name": driver_name,
                    "carNumber": car_number,
                    "carType": car_type,
                    "CarColour": car_color
                }
            }
        }
        
        return ride_data, None
    except Exception as e:
        return None, str(e)

def get_driver_passenger_ride(ride_id, passenger_id):
    """
    Get ride request details for a driver about a specific passenger
    
    Args:
        ride_id (int): ID of the ride
        passenger_id (int): ID of the passenger
        
    Returns:
        tuple: (ride_request_data, error)
    """
    try:
        # Get the passenger ride
        passenger_ride = PassengerRide.query.filter_by(
            ride_id=ride_id, 
            user_id=passenger_id
        ).first()
        
        if not passenger_ride:
            return None, f"No ride request found for passenger {passenger_id} on ride {ride_id}"
        
        # Get the ride
        ride = Ride.query.get(ride_id)
        if not ride:
            return None, f"Ride with ID {ride_id} not found"
            
        # Get the passenger
        passenger = User.query.get(passenger_id)
        if not passenger:
            return None, f"Passenger with ID {passenger_id} not found"
            
        # Format response
        ride_request_data = {
            "rideRequestDetails": {
                "requestTime": format_time_simple(ride.request_time),
                "startingLocation": ride.starting_location,
                "dropoffLocation": ride.dropoff_location,
                "Passenger_count": ride.passenger_count,
                "passengerInfo": {
                    "name": passenger.name
                }
            }
        }
        
        return ride_request_data, None
    except Exception as e:
        return None, str(e)

def get_ride_request_by_id(passenger_ride_id):
    """
    Get details of a specific ride request by ID, excluding pending status
    
    Args:
        passenger_ride_id (int): ID of the passenger ride request
        
    Returns:
        tuple: (ride_request_data, error)
    """
    try:
        # Parse the passenger_ride_id to get user_id and ride_id
        parts = passenger_ride_id.split('_')
        if len(parts) != 2:
            return None, "Invalid ride request ID format"
            
        try:
            user_id = int(parts[0])
            ride_id = int(parts[1])
        except ValueError:
            return None, "Invalid ride request ID format"
        
        # Get the passenger ride with ride and passenger information
        passenger_ride_info = PassengerRide.query\
            .filter(and_(
                PassengerRide.user_id == user_id,
                PassengerRide.ride_id == ride_id,
                PassengerRide.status != "pending"
            ))\
            .join(Ride, PassengerRide.ride_id == Ride.ride_id)\
            .join(User, PassengerRide.user_id == User.user_id)\
            .add_columns(
                User.name.label('passenger_name'),
                Ride.starting_location,
                Ride.dropoff_location,
                Ride.request_time,
                Ride.passenger_count
            ).first()
                       
        if not passenger_ride_info:
            return None, f"Ride request not found or still pending"
            
        passenger_ride = passenger_ride_info[0]  # The PassengerRide object
        passenger_name = passenger_ride_info[1]
        starting_location = passenger_ride_info[2]
        dropoff_location = passenger_ride_info[3]
        request_time = passenger_ride_info[4]
        passenger_count = passenger_ride_info[5]
        
        # Format response
        ride_request_data = {
            "rideRequestDetails": {
                "requestTime": format_time_simple(request_time),
                "startingLocation": starting_location,
                "dropoffLocation": dropoff_location,
                "Passenger_count": passenger_count,
                "passengerInfo": {
                    "name": passenger_name
                }
            }
        }
        
        return ride_request_data, None
    except Exception as e:
        return None, str(e)

def request_ride(ride_id, passenger_id, seat_count):
    """
    Create a new ride request for a passenger
    
    Args:
        ride_id (int): ID of the ride to request
        passenger_id (int): ID of the passenger making the request
        seat_count (int): Number of seats requested
        
    Returns:
        tuple: (request_data, error)
    """
    try:
        # Check if ride exists
        ride = Ride.query.get(ride_id)
        if not ride:
            return None, f"Ride with ID {ride_id} not found"
        
        # Check if passenger exists
        passenger = User.query.get(passenger_id)
        if not passenger:
            return None, f"User with ID {passenger_id} not found"
        
        # Check if passenger already requested this ride
        existing_request = PassengerRide.query.filter_by(
            user_id=passenger_id,
            ride_id=ride_id
        ).first()
        
        if existing_request:
            return None, "Passenger has already requested this ride"
        
        passenger_ride_builder = PassengerRideBuilder()
        director = Director(passenger_ride_builder)
        
        passenger_ride_data = {
            'user_id': passenger_id,
            'ride_id': ride_id,
            'status': 'pending'
        }
        
        passenger_ride = director.construct_passenger_ride(passenger_ride_data)
        
        # Explicitly set the composite primary key values
        passenger_ride.user_id = passenger_id
        passenger_ride.ride_id = ride_id
        
        db.session.add(passenger_ride)
        db.session.commit()
        
        # Format response
        request_data = {
            "rideID": ride_id,
            "passengerID": passenger_id,
            "status": "pending",
            "seatCount": seat_count
        }
        
        return request_data, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def create_ride(driver_id, starting_location, dropoff_location, passenger_count, request_time=None):
    """
    Create a new ride
    
    Args:
        driver_id (int): ID of the driver
        starting_location (str): Starting location name
        dropoff_location (str): Dropoff location name
        passenger_count (int): Number of passengers
        request_time (datetime, optional): Request time. Defaults to current time if None.
        
    Returns:
        tuple: (ride_data, error)
    """
    try:
        # Check if driver exists
        driver = Driver.query.get(driver_id)
        if not driver:
            return None, f"Driver with ID {driver_id} not found"
            
        # Use Builder pattern to create ride
        ride_builder = RideBuilder()
        director = Director(ride_builder)
        
        ride_data = {
            'driver_id': driver_id,
            'starting_location': starting_location,
            'dropoff_location': dropoff_location,
            'passenger_count': passenger_count
        }
        
        if request_time:
            ride_data['request_time'] = request_time
        
        # Construct the ride using the director
        new_ride = director.construct_ride(ride_data)
        
        db.session.add(new_ride)
        db.session.commit()
        
        # Get driver name
        driver_user = User.query.join(Driver, User.user_id == Driver.user_id)\
                    .filter(Driver.user_id == driver_id).first()
        driver_name = driver_user.name if driver_user else "Unknown Driver"
        
        # Format response
        ride_data = {
            "rideID": new_ride.ride_id,
            "driverID": new_ride.driver_id,
            "startingLocation": new_ride.starting_location,
            "dropoffLocation": new_ride.dropoff_location,
            "requestTime": new_ride.request_time.isoformat(),
            "status": new_ride.status,
            "Passenger_count": new_ride.passenger_count,
            "driverName": driver_name
        }
        
        return ride_data, None
    except Exception as e:
        db.session.rollback()
        return None, str(e) 