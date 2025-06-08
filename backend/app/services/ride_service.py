from app.models import Ride, db, User, Driver, PassengerRide
from sqlalchemy import desc, and_
from app.utils.builders import RideBuilder, PassengerRideBuilder, Director
from datetime import datetime
import logging
        

def format_time_simple(dt):
    """Format datetime to simple time format (e.g., '05:00 PM')"""
    return dt.strftime("%I:%M %p").lstrip("0")

def get_all_rides(page=1, size=20, starting_location=None, dropoff_location=None, request_time=None, seats=None):
    """
    Get all rides with pagination and filtering, excluding completed rides
    
    Args:
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        starting_location (str, optional): Filter by starting location
        dropoff_location (str, optional): Filter by dropoff location
        request_time (str, optional): Filter by request time
        seats (int, optional): Filter by available seats
        
    Returns:
        dict: Dictionary containing rides and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # Start building the query with the base filter
    query = Ride.query.filter(Ride.status != "completed")
    
    # Apply additional filters if provided
    if starting_location:
        query = query.filter(Ride.starting_location.ilike(f'%{starting_location}%'))
    
    if dropoff_location:
        query = query.filter(Ride.dropoff_location.ilike(f'%{dropoff_location}%'))
    
    if request_time:
        # Parse the time string - assuming ISO format
        try:
            time_obj = datetime.fromisoformat(request_time.replace('Z', '+00:00'))
            # Filter for rides on the same day
            from datetime import timedelta
            start_of_day = datetime(time_obj.year, time_obj.month, time_obj.day, 0, 0, 0)
            end_of_day = start_of_day + timedelta(days=1)
            query = query.filter(Ride.request_time >= start_of_day, Ride.request_time < end_of_day)
        except ValueError:
            # If date parsing fails, ignore this filter
            pass
    
    if seats and seats.isdigit():
        seats_num = int(seats)
        query = query.filter(Ride.passenger_count >= seats_num)
    
    # Get total count with filters applied
    total = query.count()
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Get rides and their drivers with all filters applied
    rides_query = db.session.query(Ride, User.name.label('driver_name'))\
        .filter(Ride.ride_id.in_([r.ride_id for r in query.all()]))\
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
        
        # Get count of approved passengers for this ride
        approved_passenger_count = PassengerRide.query.filter_by(
            ride_id=ride.ride_id,
            status="approved"
        ).count()
        
        # Skip rides that are fully booked (all seats are taken)
        if ride.passenger_count == approved_passenger_count:
            continue
        
        # Calculate available seats
        available_seats = ride.passenger_count - approved_passenger_count
        
        # Skip rides that don't have enough available seats for the requested number
        if seats and seats.isdigit() and available_seats < int(seats):
            continue
        
        formatted_rides.append({
            "rideID": ride.ride_id,
            "driverID": ride.driver_id,
            "startingLocation": ride.starting_location,
            "dropoffLocation": ride.dropoff_location,
            "requestTime": ride.request_time.isoformat(),
            "status": ride.status,
            "Passenger_count": ride.passenger_count,
            "approvedPassengerCount": approved_passenger_count,  # Add approved passenger count
            "availableSeats": available_seats,  # Add available seats count
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

def get_driver_ride_requests(driver_id):
    """
    Get all pending ride requests for a specific driver
    
    Args:
        driver_id (int): ID of the driver
        
    Returns:
        dict: Dictionary containing ride requests
    """
    try:
        # Get pending ride requests for rides driven by this driver
        requests_query = db.session.query(
            PassengerRide, 
            User.name.label('passenger_name'),
            Ride.starting_location,
            Ride.dropoff_location,
            Ride.request_time,
            Ride.ride_id
        ).join(
            Ride, PassengerRide.ride_id == Ride.ride_id
        ).join(
            User, PassengerRide.user_id == User.user_id
        ).filter(
            Ride.driver_id == driver_id,
            PassengerRide.status == "pending"
        ).order_by(desc(Ride.request_time))
        
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
        
        return {
            "requests": formatted_requests
        }
    except Exception as e:
        logging.error(f"Error in get_driver_ride_requests: {str(e)}")
        return {
            "requests": [],
            "error": str(e)
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
        
        # Check if current approved passengers + 1 would exceed the ride's capacity
        current_approved_count = PassengerRide.query.filter_by(
            ride_id=ride_id,
            status="approved"
        ).count()
        
        if current_approved_count >= ride.passenger_count:
            return None, f"Cannot approve request: Ride has reached maximum capacity of {ride.passenger_count} passengers"
        
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

def get_passenger_ride_requests(passenger_id):
    """
    Get all pending ride requests for a specific passenger
    
    Args:
        passenger_id (int): ID of the passenger
        
    Returns:
        dict: Dictionary containing ride requests
    """
    try:
        # Get all pending ride requests for this passenger
        requests_query = db.session.query(
            PassengerRide, 
            User.name.label('driver_name'),
            Ride.starting_location,
            Ride.dropoff_location,
            Ride.request_time,
            Ride.ride_id
        ).filter(
            PassengerRide.user_id == passenger_id,
            PassengerRide.status == "pending"
        ).join(Ride, PassengerRide.ride_id == Ride.ride_id)\
         .join(User, Ride.driver_id == User.user_id)\
         .order_by(desc(Ride.request_time))
        
        request_results = requests_query.all()
        
        # Format ride requests
        formatted_requests = []
        for request_info in request_results:
            passenger_ride = request_info[0]
            driver_name = request_info[1]
            starting_location = request_info[2]
            dropoff_location = request_info[3]
            request_time = request_info[4]
            ride_id = request_info[5]
            
            formatted_requests.append({
                "rideID": ride_id,
                "driverName": driver_name,
                "startingLocation": starting_location,
                "dropoffLocation": dropoff_location,
                "requestTime": format_time_simple(request_time),
                "status": passenger_ride.status
            })
        
        return {
            "requests": formatted_requests
        }
    except Exception as e:
        return {
            "requests": [],
            "error": str(e)
        }

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

def get_user_ride_history(user_id, page=1, size=20, role=None):
    """
    Get ride history for a specific user (either as passenger or driver)
    
    Args:
        user_id (int): ID of the user
        page (int): Page number (default: 1)
        size (int): Page size (default: 20)
        role (str, optional): Filter by role ('driver' or 'passenger')
        
    Returns:
        dict: Dictionary containing ride history and pagination info
    """
    # Calculate offset
    offset = (page - 1) * size
    
    # If no role specified or role is passenger, get passenger rides
    passenger_rides = []
    if role is None or role == 'passenger':
        # Get rides where user is a passenger
        passenger_query = db.session.query(
            Ride,
            PassengerRide.status.label('passenger_status'),
            User.name.label('driver_name')
        ).join(
            PassengerRide, Ride.ride_id == PassengerRide.ride_id
        ).join(
            Driver, Ride.driver_id == Driver.user_id
        ).join(
            User, Driver.user_id == User.user_id
        ).filter(
            PassengerRide.user_id == user_id
        ).order_by(
            desc(Ride.request_time)
        )
        
        # Count total passenger rides
        passenger_total = passenger_query.count()
        
        # Get paginated passenger rides
        if role is None:
            # If querying both roles, split the page size
            p_size = size // 2 if role is None else size
            passenger_results = passenger_query.offset(offset).limit(p_size).all()
        else:
            passenger_results = passenger_query.offset(offset).limit(size).all()
        
        # Format passenger rides
        for result in passenger_results:
            ride = result[0]
            passenger_status = result[1]
            driver_name = result[2] or "Unknown Driver"
            
            passenger_rides.append({
                "rideID": ride.ride_id,
                "driverID": ride.driver_id,
                "driverName": driver_name,
                "startingLocation": ride.starting_location,
                "dropoffLocation": ride.dropoff_location,
                "requestTime": ride.request_time.isoformat(),
                "status": passenger_status,  # Use passenger-specific status
                "rideType": "passenger",
                "passengerCount": ride.passenger_count
            })
    
    # If no role specified or role is driver, get driver rides
    driver_rides = []
    driver_total = 0
    if role is None or role == 'driver':
        # Get rides where user is the driver
        driver_query = db.session.query(
            Ride
        ).join(
            Driver, Ride.driver_id == Driver.user_id
        ).filter(
            Driver.user_id == user_id
        ).order_by(
            desc(Ride.request_time)
        )
        
        # Count total driver rides
        driver_total = driver_query.count()
        
        # Get paginated driver rides
        if role is None:
            # If querying both roles, split the page size and adjust offset
            d_size = size // 2 if role is None else size
            # If there are more passenger rides than the half page size, adjust driver offset
            d_offset = max(0, offset - max(0, passenger_total - p_size)) if role is None else offset
            driver_results = driver_query.offset(d_offset).limit(d_size).all()
        else:
            driver_results = driver_query.offset(offset).limit(size).all()
        
        # Format driver rides
        for ride in driver_results:
            driver_rides.append({
                "rideID": ride.ride_id,
                "driverID": ride.driver_id,
                "startingLocation": ride.starting_location,
                "dropoffLocation": ride.dropoff_location,
                "requestTime": ride.request_time.isoformat(),
                "status": ride.status,
                "rideType": "driver",
                "passengerCount": ride.passenger_count
            })
    
    # Combine and sort rides by request time
    all_rides = passenger_rides + driver_rides
    all_rides.sort(key=lambda x: x["requestTime"], reverse=True)
    
    # Reverse the order of rides (so row 3 becomes row 1, etc.)
    all_rides = all_rides[::-1]
    
    # Calculate total across both types
    total = passenger_total + driver_total if role is None else (passenger_total if role == 'passenger' else driver_total)
    
    # Calculate total pages
    total_pages = (total + size - 1) // size if total > 0 else 1
    
    # Calculate pagination values
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None
    
    return {
        "rides": all_rides[:size],  # Limit to page size after sorting
        "pagination": {
            "currentPage": page,
            "pageSize": size,
            "totalPages": total_pages,
            "totalRides": total,
            "nextPage": next_page,
            "prevPage": prev_page
        }
    }

def get_ride_details_with_passengers(ride_id, user_role='passenger'):
    """
    Get detailed information about a ride including all passenger details
    
    Args:
        ride_id (int): ID of the ride to retrieve
        user_role (str): Role of the requesting user ('driver' or 'passenger')
        
    Returns:
        dict: Dictionary containing ride details and passenger information
    """
    # Get the ride details
    ride = Ride.query.get(ride_id)
    if not ride:
        return None
    
    # Get driver details
    driver_info = None
    car_info = None
    if ride.driver_id:
        driver = User.query.join(Driver, User.user_id == Driver.user_id).filter(Driver.user_id == ride.driver_id).first()
        driver_details = Driver.query.filter_by(user_id=ride.driver_id).first()
        
        if driver:
            driver_info = {
                "driverID": driver.user_id,
                "name": driver.name,
                "email": driver.email,
                "phone": driver.phone
            }
        
        if driver_details:
            car_info = {
                "carNumber": driver_details.car_number,
                "carType": driver_details.car_type,
                "carColor": driver_details.car_color
            }
    
    # Get all passenger rides for this ride
    passenger_rides = PassengerRide.query.filter_by(ride_id=ride_id).all()
    
    # Get passenger details for each passenger ride
    passengers = []
    for passenger_ride in passenger_rides:
        # Filter passengers based on user role
        if user_role == 'driver':
            # For drivers, include approved/accepted/active/completed passengers
            # but filter out pending, rejected, cancelled statuses
            if passenger_ride.status not in ['approved', 'accepted', 'active', 'completed']:
                continue
        
        # Get passenger information
        passenger = User.query.get(passenger_ride.user_id)
        if passenger:
            # Create a unique identifier for this passenger ride 
            # using the composite key (user_id and ride_id)
            passenger_ride_id = f"{passenger_ride.user_id}_{passenger_ride.ride_id}"
            
            passengers.append({
                "passengerID": passenger.user_id,
                "name": passenger.name,
                "email": passenger.email,
                "phone": passenger.phone,
                "status": passenger_ride.status,
                "passengerRideID": passenger_ride_id
            })
    
    # Format ride details with passengers
    ride_details = {
        "rideID": ride.ride_id,
        "driverID": ride.driver_id,
        "startingLocation": ride.starting_location,
        "dropoffLocation": ride.dropoff_location,
        "requestTime": ride.request_time.isoformat(),
        "status": ride.status,
        "passengerCount": ride.passenger_count,
        "driver": driver_info,
        "car": car_info,
        "passengers": passengers
    }
    
    return ride_details

def reject_ride_request(ride_id, passenger_id):
    """
    Reject a ride request
    
    Args:
        ride_id (int): ID of the ride
        passenger_id (int): ID of the passenger
        
    Returns:
        tuple: (result, error)
    """
    try:
        # Get the passenger ride
        passenger_ride = PassengerRide.query.filter_by(
            ride_id=ride_id, 
            user_id=passenger_id,
            status='pending'
        ).first()
        
        if not passenger_ride:
            return None, "Ride request not found or already processed"
        
        # Update the passenger ride status
        passenger_ride.status = 'rejected'
        db.session.commit()
        
        return passenger_ride, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def cancel_ride_request(ride_id, passenger_id):
    """
    Cancel a passenger's ride request
    
    Args:
        ride_id (int): ID of the ride
        passenger_id (int): ID of the passenger
        
    Returns:
        tuple: (result, error)
    """
    try:
        # Get the passenger ride
        passenger_ride = PassengerRide.query.filter_by(
            ride_id=ride_id, 
            user_id=passenger_id,
            status='pending'
        ).first()
        
        if not passenger_ride:
            return None, "Ride request not found or already processed"
        
        # Update the passenger ride status to cancelled
        passenger_ride.status = 'cancelled'
        db.session.commit()
        
        return passenger_ride, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def complete_ride(ride_id, passenger_id):
    """
    Mark a ride as completed for a passenger
    
    Args:
        ride_id (int): ID of the ride
        passenger_id (int): ID of the passenger
        
    Returns:
        tuple: (completion_data, error)
    """
    try:
        # Verify ride exists
        ride = Ride.query.get(ride_id)
        if not ride:
            return None, f"Ride with ID {ride_id} not found"
        
        # Verify passenger exists
        passenger = User.query.get(passenger_id)
        if not passenger:
            return None, f"Passenger with ID {passenger_id} not found"
        
        # Find the passenger ride request
        passenger_ride = PassengerRide.query.filter_by(
            ride_id=ride_id,
            user_id=passenger_id
        ).first()
        
        if not passenger_ride:
            return None, f"No ride request found for passenger {passenger_id} on ride {ride_id}"
        
        # Check if the ride request is already completed
        if passenger_ride.status == "completed":
            return None, "Ride is already marked as completed"
        
        # Check if the ride request is in a state that can be completed
        if passenger_ride.status not in ["approved", "accepted", "active"]:
            return None, f"Ride request with status '{passenger_ride.status}' cannot be completed"
        
        # Update the passenger ride status to completed
        passenger_ride.status = "completed"
        db.session.commit()
        
        # Check if all passengers have completed the ride
        all_completed = True
        for pr in PassengerRide.query.filter_by(ride_id=ride_id).all():
            if pr.status != "completed" and pr.status != "rejected" and pr.status != "cancelled":
                all_completed = False
                break
        
        # If all passengers have completed, mark the ride as completed
        if all_completed:
            ride.status = "completed"
            db.session.commit()
        
        return {
            "message": "Ride marked as completed successfully",
            "rideID": ride_id,
            "passengerID": passenger_id,
            "status": "completed"
        }, None
        
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def get_homepage_data(user_id):
    """
    Get homepage data including total rides, pending requests, and recent activity
    
    Args:
        user_id (int): ID of the user
        
    Returns:
        dict: Dictionary containing homepage data
    """
    try:
        # Get user role
        from app.models import UserRole
        user_role = UserRole.query.filter_by(user_id=user_id).first()
        role = user_role.role_name if user_role else "passenger"
        
        result = {
            "total_rides": 0,
            "pending_requests": 0,
            "recent_notifications": []
        }
        
        # Get total rides based on role
        if role == "driver":
            # For drivers: count rides they've created
            result["total_rides"] = Ride.query.filter_by(driver_id=user_id).count()
            
            # For drivers: count pending ride requests they've received
            driver_rides = Ride.query.filter_by(driver_id=user_id).all()
            ride_ids = [ride.ride_id for ride in driver_rides]
            
            if ride_ids:
                result["pending_requests"] = PassengerRide.query.filter(
                    PassengerRide.ride_id.in_(ride_ids),
                    PassengerRide.status == "pending"
                ).count()
        else:
            # For passengers: count rides they've participated in
            result["total_rides"] = PassengerRide.query.filter_by(user_id=user_id).count()
            
            # For passengers: count their pending ride requests
            result["pending_requests"] = PassengerRide.query.filter_by(
                user_id=user_id,
                status="pending"
            ).count()
        
        # Get recent notifications
        from app.models import Notification
        notifications = Notification.query.filter_by(user_id=user_id)\
            .order_by(Notification.time.desc())\
            .limit(5)\
            .all()
        
        # Format notifications
        for notification in notifications:
            result["recent_notifications"].append({
                "id": notification.notification_id,
                "message": notification.message,
                "created_at": notification.time.isoformat(),
                "is_read": notification.read
            })
        
        return result
    except Exception as e:
        logging.error(f"Error in get_homepage_data: {str(e)}")
        return {
            "total_rides": 0,
            "pending_requests": 0,
            "recent_notifications": [],
            "error": str(e)
        } 