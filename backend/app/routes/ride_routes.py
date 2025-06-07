from flask import Blueprint, request, jsonify
from app.services import ride_service, notification_service, chat_service
from app.utils.jwt_handler import token_required, role_required
from app.models import User, db, Ride, Driver, PassengerRide, Passenger
from datetime import datetime
import logging
from app.utils.filter_strategies import get_filter_context_instance, FILTER_STRATEGY_MAP

ride_bp = Blueprint('rides', __name__)

@ride_bp.route('', methods=['GET'])
def get_rides():
    """Get all rides with pagination and filtering (excluding completed rides)"""
    # Get pagination parameters
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    
    # Validate pagination parameters
    if page < 1 or size < 1:
        return jsonify({"error": "Page and size must be positive integers"}), 400
    
    # Get filter parameters
    starting_location = request.args.get('starting_location', None)
    dropoff_location = request.args.get('dropoff_location', None)
    request_time = request.args.get('request_time', None)
    seats = request.args.get('seats', None)
    
    # Get rides with filters applied
    rides_data = ride_service.get_all_rides(
        page, 
        size, 
        starting_location, 
        dropoff_location, 
        request_time, 
        seats
    )
    
    return jsonify(rides_data), 200

@ride_bp.route('/<int:ride_id>', methods=['GET'])
@token_required
def get_ride_by_id(ride_id):
    """Get a specific ride by ID"""
    try:
        # Query the ride
        ride = Ride.query.get(ride_id)
        
        # Check if ride exists
        if not ride:
            return jsonify({"error": f"Ride with ID {ride_id} not found"}), 404
        
        # Get driver info
        driver = User.query.join(Driver).filter(Driver.user_id == ride.driver_id).first()
        driver_name = driver.name if driver else "Unknown"
        
        # Get driver's car information
        driver_info = Driver.query.filter_by(user_id=ride.driver_id).first()
        car_number = driver_info.car_number if driver_info else "Unknown"
        car_type = driver_info.car_type if driver_info else "Unknown"
        
        # Get the current user's ID
        user_id = request.user.user_id

        # Default status is the ride's status
        status = ride.status
        # Check if the user is a passenger by querying the Passenger table
        is_passenger = Passenger.query.filter_by(user_id=user_id).first() is not None
        # If the user is a passenger, get their specific status for this ride
        print("--------------------------------")
        print(ride_id)
        if is_passenger:
            passenger_ride = PassengerRide.query.filter_by(
                ride_id=ride_id,
                user_id=user_id
            ).first()
            
            if passenger_ride:
                status = passenger_ride.status
        # Format the response
        ride_data = {
            "rideID": ride.ride_id,
            "driverID": ride.driver_id,
            "driverName": driver_name,
            "startingLocation": ride.starting_location,
            "dropoffLocation": ride.dropoff_location,
            "requestTime": ride.request_time.isoformat(),
            "Passenger_count": ride.passenger_count,
            "seatsOccupied": ride.seats_occupied if hasattr(ride, 'seats_occupied') else 0,
            "status": status,
            "carNumber": car_number,
            "carType": car_type
        }
        
        return jsonify(ride_data), 200
    except Exception as e:
        logging.error(f"get_ride_by_id error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ride_bp.route('/<int:ride_id>/passenger/<int:passenger_id>', methods=['GET'])
@role_required(['driver'])
def get_passenger_ride_details(ride_id, passenger_id):
    """Get details of a passenger's ride request for a specific ride"""
    # Get ride request details
    ride_request_data, error = ride_service.get_driver_passenger_ride(ride_id, passenger_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(ride_request_data), 200

@ride_bp.route('/requests/approve', methods=['POST'])
@role_required(['driver'])
def approve_ride_request():
    """Approve a passenger's ride request"""
    # Get the driver ID from the authenticated user
    driver_id = request.user.user_id
    
    # Get request data
    data = request.json
    
    # Validate required fields
    required_fields = ['rideID', 'passengerID']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    ride_id = data['rideID']
    passenger_id = data['passengerID']
    
    # Approve the ride request
    result, error = ride_service.approve_ride_request(
        ride_id=ride_id,
        passenger_id=passenger_id,
        driver_id=driver_id
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Get ride and user details for notification
    ride = Ride.query.get(ride_id)
    driver = User.query.get(driver_id)
    
    if ride and driver:
        # Create notification for the passenger
        notification_service.notify_ride_request_approved(
            ride_id=ride_id,
            driver_id=driver_id,
            driver_name=driver.name,
            passenger_id=passenger_id,
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
    
    return jsonify({"message": "Ride request approved successfully"}), 200

@ride_bp.route('/requests/reject', methods=['POST'])
@role_required(['driver'])
def reject_ride_request():
    """Reject a passenger's ride request"""
    # Get the driver ID from the authenticated user
    driver_id = request.user.user_id
    
    # Get request data
    data = request.json
    
    # Validate required fields
    required_fields = ['rideID', 'passengerID']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    ride_id = data['rideID']
    passenger_id = data['passengerID']
    
    # Reject the ride request
    result, error = ride_service.reject_ride_request(
        ride_id=ride_id,
        passenger_id=passenger_id
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Get ride and user details for notification
    ride = Ride.query.get(ride_id)
    driver = User.query.get(driver_id)
    
    if ride and driver:
        # Create notification for the passenger
        notification_service.notify_ride_request_rejected(
            ride_id=ride_id,
            driver_id=driver_id,
            driver_name=driver.name,
            passenger_id=passenger_id,
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
    
    return jsonify({"message": "Ride request rejected successfully"}), 200

@ride_bp.route('/driver/<int:driver_id>/requests', methods=['GET'])
@role_required(['driver'])
def get_driver_ride_requests(driver_id):
    """Get all pending ride requests for a specific driver"""
    try:
        # Get the authenticated user's ID
        auth_user_id = request.user.user_id
        
        # Ensure the authenticated driver is requesting their own ride requests
        if auth_user_id != driver_id:
            return jsonify({"error": "You can only view your own ride requests"}), 403
        
        # Get ride requests
        requests_data = ride_service.get_driver_ride_requests(driver_id)
        
        return jsonify(requests_data), 200
    except Exception as e:
        logging.error(f"Error in get_driver_ride_requests route: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@ride_bp.route('/requests/<string:passenger_ride_id>', methods=['GET'])
@token_required
def get_ride_request_details(passenger_ride_id):
    """Get details of a specific ride request by ID"""
    # Get ride request details
    ride_request_data, error = ride_service.get_ride_request_by_id(passenger_ride_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(ride_request_data), 200

@ride_bp.route('/requests', methods=['POST'])
@role_required(['passenger'])
def request_ride():
    """Request to join a ride as a passenger"""
    # Get request data
    data = request.json
    
    # Validate required fields
    required_fields = ['rideID', 'passengerID', 'seatCount']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate seat count
    seat_count = data.get('seatCount')
    if not isinstance(seat_count, int) or seat_count < 1:
        return jsonify({"error": "seatCount must be a positive integer"}), 400
    
    # Create ride request
    request_data, error = ride_service.request_ride(
        ride_id=data['rideID'],
        passenger_id=data['passengerID'],
        seat_count=data['seatCount']
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Get ride details for notification
    ride = Ride.query.get(data['rideID'])
    passenger = User.query.get(data['passengerID'])
    
    if ride and passenger:
        # Create notification for the driver
        notification_service.notify_ride_request(
            ride_id=data['rideID'],
            driver_id=ride.driver_id,
            passenger_id=data['passengerID'],
            passenger_name=passenger.name,
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
        
        # Create notification for the passenger
        notification_service.notify_ride_request_submitted(
            passenger_id=data['passengerID'],
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
    
    return jsonify(request_data), 201

@ride_bp.route('', methods=['POST'])
@role_required(['driver'])
def create_ride():
    """Create a new ride"""
    try:
        # Get request data
        data = request.json
        
        # Log the authenticated user
        user = request.user
        logging.info(f"Create ride request from user: {user.user_id} ({user.name})")
        
        # Validate required fields
        required_fields = ['driverID', 'startingLocation', 'dropoffLocation', 'Passenger_count']
        for field in required_fields:
            if field not in data:
                logging.warning(f"Missing required field in create_ride: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate location format
        for location_field in ['startingLocation', 'dropoffLocation']:
            location = data.get(location_field)
            if not isinstance(location, str) or not location.strip():
                logging.warning(f"Invalid {location_field} format: {location}")
                return jsonify({"error": f"{location_field} must be a non-empty string"}), 400
        
        # Get driver ID from request body
        try:
            driver_id = int(data['driverID'])
        except (ValueError, TypeError):
            logging.warning(f"Invalid driverID format: {data['driverID']}")
            return jsonify({"error": "driverID must be an integer"}), 400
        
        # Ensure driver_id matches authenticated user
        if driver_id != user.user_id:
            logging.warning(f"Driver ID mismatch: {driver_id} vs authenticated user {user.user_id}")
            return jsonify({"error": "Driver ID must match authenticated user"}), 403
        
        # Parse requestTime if provided, otherwise use current time
        request_time = None
        if 'requestTime' in data and data['requestTime']:
            try:
                request_time = datetime.fromisoformat(data['requestTime'].replace('Z', '+00:00'))
            except ValueError:
                logging.warning(f"Invalid requestTime format: {data['requestTime']}")
                return jsonify({"error": "Invalid requestTime format. Use ISO format (e.g. 2025-05-29T17:00:00)"}), 400
        
        logging.info(f"Creating ride: driver={driver_id}, from={data['startingLocation']}, to={data['dropoffLocation']}")
        
        # Create ride
        ride_data, error = ride_service.create_ride(
            driver_id=driver_id,
            starting_location=data['startingLocation'],
            dropoff_location=data['dropoffLocation'],
            passenger_count=data['Passenger_count'],
            request_time=request_time
        )
        
        if error:
            logging.error(f"Failed to create ride: {error}")
            return jsonify({"error": error}), 400
        
        logging.info(f"Ride created successfully: {ride_data['rideID']}")
        
        # Create chat for the ride using chat service
        chat_data, chat_error = chat_service.create_chat_for_ride(ride_data['rideID'])
        if chat_error:
            # Log the error but continue with ride creation
            logging.warning(f"Failed to create chat for ride {ride_data['rideID']}: {chat_error}")
        else:
            logging.info(f"Chat created for ride {ride_data['rideID']}")
        
        # Get driver details for notification
        driver = User.query.get(driver_id)
        
        if driver:
            # Create notification for the driver about ride publication
            notification_service.notify_ride_published(
                driver_id=driver_id,
                driver_name=driver.name,
                from_location=data['startingLocation'],
                to_location=data['dropoffLocation']
            )
            logging.info(f"Notification sent for ride publication: driver={driver_id}")
        
        return jsonify(ride_data), 201
    except Exception as e:
        logging.exception(f"Unexpected error in create_ride: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@ride_bp.route('/user-history', methods=['GET'])
@token_required
def get_user_ride_history():
    """Get ride history for the authenticated user"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Get query parameters
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    
    # Validate pagination parameters
    if page < 1 or size < 1:
        return jsonify({"error": "Page and size must be positive integers"}), 400
    
    # Get role filter if provided
    role = request.args.get('role', None)
    if role not in [None, 'driver', 'passenger']:
        return jsonify({"error": "Role must be either 'driver' or 'passenger'"}), 400
    
    # Get user ride history
    history_data = ride_service.get_user_ride_history(
        user_id=user_id,
        page=page,
        size=size,
        role=role
    )
    
    return jsonify(history_data), 200

@ride_bp.route('/<int:ride_id>/details', methods=['GET'])
@token_required
def get_ride_details_with_passengers(ride_id):
    """Get detailed ride information including all passengers"""
    # Get the user ID from the authenticated user
    user_id = request.user.user_id
    
    # Get detailed ride information
    ride_details = ride_service.get_ride_details_with_passengers(ride_id)
    
    if not ride_details:
        return jsonify({"error": "Ride not found"}), 404
    
    # Check if user is authorized to view details
    # Allow if user is the driver or one of the passengers
    is_driver = ride_details["driverID"] == user_id
    is_passenger = any(p["passengerID"] == user_id for p in ride_details["passengers"])
    
    if not (is_driver or is_passenger):
        return jsonify({"error": "You are not authorized to view this ride's details"}), 403
    
    return jsonify(ride_details), 200

@ride_bp.route('/passenger/<int:passenger_id>/requests', methods=['GET'])
@role_required(['passenger'])
def get_passenger_ride_requests(passenger_id):
    """Get all pending ride requests for a specific passenger"""
    # Get ride requests
    requests_data = ride_service.get_passenger_ride_requests(passenger_id)
    
    return jsonify(requests_data), 200

@ride_bp.route('/<int:ride_id>/cancel', methods=['POST'])
@role_required(['passenger'])
def cancel_ride_request(ride_id):
    """Cancel a passenger's ride request"""
    # Get the passenger ID from the authenticated user
    passenger_id = request.user.user_id
    
    # Cancel the ride request
    result, error = ride_service.cancel_ride_request(
        ride_id=ride_id,
        passenger_id=passenger_id
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Get ride and user details for notification
    ride = Ride.query.get(ride_id)
    passenger = User.query.get(passenger_id)
    
    if ride and passenger:
        # Create notification for the driver
        notification_service.notify_ride_request_cancelled(
            ride_id=ride_id,
            driver_id=ride.driver_id,
            passenger_id=passenger_id,
            passenger_name=passenger.name,
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
        
        # Create notification for the passenger
        notification_service.notify_ride_request_cancelled_passenger(
            passenger_id=passenger_id,
            from_location=ride.starting_location,
            to_location=ride.dropoff_location
        )
    
    return jsonify({"message": "Ride request cancelled successfully"}), 200

@ride_bp.route('/<int:ride_id>/complete', methods=['POST'])
@role_required(['passenger'])
def complete_ride(ride_id):
    """Mark a ride as completed by a passenger"""
    # Get the passenger ID from the authenticated user
    passenger_id = request.user.user_id
    
    # Complete the ride
    result, error = ride_service.complete_ride(
        ride_id=ride_id,
        passenger_id=passenger_id
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    # Create notification for the driver
    try:
        # Get ride details
        ride = Ride.query.get(ride_id)
        passenger = User.query.get(passenger_id)
        
        if ride and passenger:
            # Create notification for the driver
            notification_service.create_notification(
                user_id=ride.driver_id,
                message=f"{passenger.name} has completed the ride from {ride.starting_location} to {ride.dropoff_location}."
            )
    except Exception as e:
        # Log the error but don't fail the request
        print(f"Error creating notification: {str(e)}")
    
    return jsonify(result), 200

@ride_bp.route('/homepage', methods=['GET'])
@token_required
def get_homepage_data():
    """Get homepage data including total rides, pending requests, and recent activity"""
    try:
        # Get the user ID from the authenticated user
        user_id = request.user.user_id
        
        # Get homepage data
        homepage_data = ride_service.get_homepage_data(user_id)
        
        return jsonify(homepage_data), 200
    except Exception as e:
        logging.error(f"Error in get_homepage_data route: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@ride_bp.route('/filter', methods=['GET'])
@token_required
def filter_rides():
    """
    Filter rides based on status, time, or date
    
    Query parameters:
    - filter_type: The type of filter to apply ('status', 'time', 'date')
    - criteria: The filter criteria value
    - page: Page number (default: 1)
    - size: Page size (default: 20)
    """
    try:
        # Get the user ID from the authenticated user
        user_id = request.user.user_id
        
        # Get query parameters
        filter_type = request.args.get('filter_type')
        criteria = request.args.get('criteria')
        
        try:
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 20))
        except ValueError:
            return jsonify({"error": "Invalid pagination parameters"}), 400
        
        # Validate pagination parameters
        if page < 1 or size < 1:
            return jsonify({"error": "Page and size must be positive integers"}), 400
        
        # Get user ride history
        history_data = ride_service.get_user_ride_history(
            user_id=user_id,
            page=1,  # Get all rides for filtering, we'll paginate after filtering
            size=1000,  # Use a large number to get all rides
            role=None  # Don't filter by role, get all rides for the user
        )
        
        rides = history_data.get('rides', [])
        
        # If no filter type or criteria is provided, return the unfiltered rides with pagination
        if not filter_type or not criteria:
            # Apply pagination after getting all rides
            start_idx = (page - 1) * size
            end_idx = start_idx + size
            paginated_rides = rides[start_idx:end_idx] if start_idx < len(rides) else []
            
            return jsonify({
                "rides": paginated_rides,
                "pagination": {
                    "currentPage": page,
                    "pageSize": size,
                    "totalPages": (len(rides) + size - 1) // size if rides else 1,
                    "totalRides": len(rides),
                    "nextPage": page + 1 if end_idx < len(rides) else None,
                    "prevPage": page - 1 if page > 1 else None
                }
            }), 200
        
        # Check if the filter type exists in the map
        if filter_type not in FILTER_STRATEGY_MAP:
            return jsonify({"error": f"Invalid filter type: {filter_type}. Valid types are: {', '.join(FILTER_STRATEGY_MAP.keys())}"}), 400
        
        # Get the global filter context instance
        filter_context = get_filter_context_instance()
        
        # Set the appropriate filter strategy based on the filter type
        filter_strategy_class = FILTER_STRATEGY_MAP[filter_type]
        filter_context.set_filter_strategy(filter_strategy_class())
        
        # Filter the rides using the selected strategy
        filtered_rides = filter_context.filter_rides(rides, criteria)
        
        # Apply pagination after filtering
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_rides = filtered_rides[start_idx:end_idx] if start_idx < len(filtered_rides) else []
        
        return jsonify({
            "rides": paginated_rides,
            "pagination": {
                "currentPage": page,
                "pageSize": size,
                "totalPages": (len(filtered_rides) + size - 1) // size if filtered_rides else 1,
                "totalRides": len(filtered_rides),
                "nextPage": page + 1 if end_idx < len(filtered_rides) else None,
                "prevPage": page - 1 if page > 1 else None
            }
        }), 200
    except Exception as e:
        logging.error(f"Error in filter_rides route: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

 