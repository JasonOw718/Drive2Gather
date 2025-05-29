from app.models import Ride, db, User, Driver
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import joinedload

def format_time_simple(dt):
    """Format datetime to simple time format (e.g., '05:00 PM')"""
    return dt.strftime("%I:%M %p").lstrip("0")

def get_all_rides(page=1, size=20):
    """
    Get all rides with pagination
    
    Args:
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        
    Returns:
        dict: Dictionary containing rides and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Get total count
    total = Ride.query.count()
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Get rides for current page with driver information
    rides = Ride.query.join(Driver, Ride.driver_id == Driver.user_id)\
                .join(User, Driver.user_id == User.user_id)\
                .order_by(desc(Ride.request_time))\
                .add_columns(User.name.label('driver_name'))\
                .offset(offset).limit(size).all()
    
    # Format rides
    formatted_rides = []
    for ride_info in rides:
        ride = ride_info[0]  # The Ride object
        driver_name = ride_info[1]  # The driver name
        
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

def get_ride_by_id(ride_id):
    """
    Get details of a specific ride by ID
    
    Args:
        ride_id (int): ID of the ride
        
    Returns:
        tuple: (ride_data, error)
    """
    try:
        # Get the ride with driver information
        ride_info = Ride.query.join(Driver, Ride.driver_id == Driver.user_id)\
                       .join(User, Driver.user_id == User.user_id)\
                       .filter(Ride.ride_id == ride_id)\
                       .add_columns(
                           User.name.label('driver_name'),
                           Driver.car_number.label('car_number'),
                           Driver.car_type.label('car_type'),
                           Driver.car_color.label('car_color')
                       ).first()
                       
        if not ride_info:
            return None, f"Ride with ID {ride_id} not found"
            
        ride = ride_info[0]  # The Ride object
        driver_name = ride_info[1]
        car_number = ride_info[2]
        car_type = ride_info[3]
        car_color = ride_info[4]
        
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
        # Use provided request_time or current time
        if request_time is None:
            request_time = datetime.utcnow()
        
        # Create new ride
        new_ride = Ride(
            driver_id=driver_id,
            starting_location=starting_location,
            dropoff_location=dropoff_location,
            request_time=request_time,
            status="pending",
            passenger_count=passenger_count
        )
        
        db.session.add(new_ride)
        db.session.commit()
        
        # Get driver name
        driver = User.query.join(Driver, User.user_id == Driver.user_id)\
                    .filter(Driver.user_id == driver_id).first()
        driver_name = driver.name if driver else "Unknown Driver"
        
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