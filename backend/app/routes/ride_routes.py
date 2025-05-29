from flask import Blueprint, request, jsonify
from app.services import ride_service
from app.utils.jwt_handler import token_required, role_required

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

@ride_bp.route('', methods=['POST'])
@role_required(['driver'])
def create_ride():
    """Create a new ride (driver only)"""
    # Get the driver ID from the authenticated user
    driver_id = request.user.user_id
    
    # Get request data
    data = request.json
    
    # Validate required fields
    required_fields = ['startingLocation', 'dropoffLocation', 'passenger_count', 'fare']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate location format
    for location_field in ['startingLocation', 'dropoffLocation']:
        location = data.get(location_field)
        if not isinstance(location, dict) or 'lat' not in location or 'lng' not in location:
            return jsonify({"error": f"{location_field} must contain lat and lng coordinates"}), 400
    
    # Create ride
    ride_data, error = ride_service.create_ride(
        driver_id=driver_id,
        starting_location=data['startingLocation'],
        dropoff_location=data['dropoffLocation'],
        passenger_count=data['passenger_count'],
        fare=data['fare']
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(ride_data), 201 