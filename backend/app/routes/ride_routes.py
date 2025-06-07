from flask import Blueprint, request, jsonify
from app.services import ride_service
from app.utils.jwt_handler import token_required, role_required
from app.models import User, db, Ride, Driver
from datetime import datetime

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
            "fare": float(ride.fare) if hasattr(ride, 'fare') else 0.0,
            "status": ride.status
        }
        
        return jsonify(ride_data), 200
    except Exception as e:
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
    
    return jsonify({"message": "Ride request rejected successfully"}), 200

@ride_bp.route('/driver/<int:driver_id>/requests', methods=['GET'])
@role_required(['driver'])
def get_driver_ride_requests(driver_id):
    """Get all pending ride requests for a specific driver"""
    # Get ride requests
    requests_data = ride_service.get_driver_ride_requests(driver_id)
    
    return jsonify(requests_data), 200

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
    
    return jsonify(request_data), 201

@ride_bp.route('', methods=['POST'])
@role_required(['driver'])
def create_ride():
    """Create a new ride"""
    # Get request data
    data = request.json
    
    # Validate required fields
    required_fields = ['driverID', 'startingLocation', 'dropoffLocation', 'Passenger_count']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate location format
    for location_field in ['startingLocation', 'dropoffLocation']:
        location = data.get(location_field)
        if not isinstance(location, str) or not location.strip():
            return jsonify({"error": f"{location_field} must be a non-empty string"}), 400
    
    # Get driver ID from request body
    driver_id = data['driverID']
    
    # Parse requestTime if provided, otherwise use current time
    request_time = None
    if 'requestTime' in data and data['requestTime']:
        try:
            request_time = datetime.fromisoformat(data['requestTime'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({"error": "Invalid requestTime format. Use ISO format (e.g. 2025-05-29T17:00:00)"}), 400
    
    # Create ride
    ride_data, error = ride_service.create_ride(
        driver_id=driver_id,
        starting_location=data['startingLocation'],
        dropoff_location=data['dropoffLocation'],
        passenger_count=data['Passenger_count'],
        request_time=request_time
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(ride_data), 201

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

 