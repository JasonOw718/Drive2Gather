from datetime import datetime
import re

# Strategy Interface
class FilterStrategy:
    def filter(self, rides, criteria):
        pass

# Concrete Strategies
class FilterByStatus(FilterStrategy):
    def filter(self, rides, criteria):
        if not criteria:
            return rides
        return [ride for ride in rides if ride.get('status', '').lower() == criteria.lower()]

class FilterByTime(FilterStrategy):
    def filter(self, rides, criteria):
        if not criteria:
            return rides
        
        # Criteria should be in format "HH:MM"
        time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$')
        if not time_pattern.match(criteria):
            return []
        
        # Extract the hour and minute from the criteria
        hour, minute = criteria.split(':')
        hour, minute = int(hour), int(minute)
        
        filtered_rides = []
        for ride in rides:
            request_time = ride.get('requestTime')
            if request_time:
                try:
                    # Parse the ISO format datetime
                    dt = datetime.fromisoformat(request_time.replace('Z', '+00:00'))
                    # Check if the hour and minute match
                    if dt.hour == hour and dt.minute == minute:
                        filtered_rides.append(ride)
                except (ValueError, AttributeError):
                    # Skip rides with invalid datetime format
                    continue
        
        return filtered_rides

class FilterByDate(FilterStrategy):
    def filter(self, rides, criteria):
        if not criteria:
            return rides
        
        # Criteria should be in format "YYYY-MM-DD"
        try:
            target_date = datetime.strptime(criteria, "%Y-%m-%d").date()
        except ValueError:
            return []
        
        filtered_rides = []
        for ride in rides:
            request_time = ride.get('requestTime')
            if request_time:
                try:
                    # Parse the ISO format datetime
                    dt = datetime.fromisoformat(request_time.replace('Z', '+00:00'))
                    # Check if the date matches
                    if dt.date() == target_date:
                        filtered_rides.append(ride)
                except (ValueError, AttributeError):
                    # Skip rides with invalid datetime format
                    continue
        
        return filtered_rides

# Context (FilterContext)
class FilterContext:
    def __init__(self, filter_strategy: FilterStrategy):
        self.filter_strategy = filter_strategy
    
    def set_filter_strategy(self, strategy: FilterStrategy):
        self.filter_strategy = strategy
    
    def filter_rides(self, rides, criteria):
        return self.filter_strategy.filter(rides, criteria)

# Singleton instance of FilterContext
filter_context_instance = None

def get_filter_context_instance():
    global filter_context_instance
    if filter_context_instance is None:
        filter_context_instance = FilterContext(FilterByStatus())  # Default strategy
    return filter_context_instance

# Mapping filter types to strategy classes
FILTER_STRATEGY_MAP = {
    'status': FilterByStatus,
    'time': FilterByTime,
    'date': FilterByDate
} 