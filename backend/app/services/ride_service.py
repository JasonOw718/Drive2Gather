from app.models import Ride, db
from datetime import datetime
from sqlalchemy import desc

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
    
    # Get rides for current page
    rides = Ride.query.order_by(desc(Ride.request_time)).offset(offset).limit(size).all()
    
    # Format rides
    formatted_rides = []
    for ride in rides:
        formatted_rides.append({
            "rideID": ride.ride_id,
            "driverID": ride.driver_id,
            "startingLocation": ride.starting_location,
            "dropoffLocation": ride.dropoff_location,
            "requestTime": ride.request_time.isoformat() + "Z",
            "status": ride.status,
            "passenger_count": ride.passenger_count,
            "fare": ride.fare
        })
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "rides": formatted_rides
    }

def create_ride(driver_id, starting_location, dropoff_location, passenger_count, fare):
    """
    Create a new ride
    
    Args:
        driver_id (int): ID of the driver
        starting_location (dict): Starting location coordinates
        dropoff_location (dict): Dropoff location coordinates
        passenger_count (int): Number of passengers
        fare (float): Fare amount
        
    Returns:
        tuple: (ride_data, error)
    """
    try:
        # Create new ride
        new_ride = Ride(
            driver_id=driver_id,
            starting_location=starting_location,
            dropoff_location=dropoff_location,
            request_time=datetime.utcnow(),
            status="pending",
            passenger_count=passenger_count,
            fare=fare
        )
        
        db.session.add(new_ride)
        db.session.commit()
        
        # Format response
        ride_data = {
            "rideID": new_ride.ride_id,
            "driverID": new_ride.driver_id,
            "startingLocation": new_ride.starting_location,
            "dropoffLocation": new_ride.dropoff_location,
            "requestTime": new_ride.request_time.isoformat() + "Z",
            "status": new_ride.status,
            "passenger_count": new_ride.passenger_count,
            "fare": new_ride.fare
        }
        
        return ride_data, None
    except Exception as e:
        db.session.rollback()
        return None, str(e) 