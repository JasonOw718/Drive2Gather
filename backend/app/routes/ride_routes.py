from flask import Blueprint, request, jsonify
from app.services import ride_service
from app.utils.jwt_handler import token_required, role_required
from app.models import User, db
from datetime import datetime

ride_bp = Blueprint('rides', __name__)

@ride_bp.route('', methods=['GET'])
@token_required
def get_rides():
    """Get all rides with pagination"""
    # Get pagination parameters
    try:
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    
    # Validate pagination parameters
    if page < 1 or size < 1:
        return jsonify({"error": "Page and size must be positive integers"}), 400
    
    # Get rides
    rides_data = ride_service.get_all_rides(page, size)
    
    return jsonify(rides_data), 200

@ride_bp.route('/<int:ride_id>', methods=['GET'])
@token_required
def get_ride_details(ride_id):
    """Get details of a specific ride by ID"""
    # Get ride details
    ride_data, error = ride_service.get_ride_by_id(ride_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(ride_data), 200

@ride_bp.route('', methods=['POST'])
@token_required
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