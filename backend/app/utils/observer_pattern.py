from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, data: Dict[str, Any]) -> None:
        """
        Update method that gets called when the subject changes
        
        Args:
            data: Dictionary containing notification data
        """
        pass

# Subject (Observable) Interface
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject
        
        Args:
            observer: The observer to attach
        """
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject
        
        Args:
            observer: The observer to detach
        """
        pass
    
    @abstractmethod
    def notify(self, data: Dict[str, Any]) -> None:
        """
        Notify all observers about an event
        
        Args:
            data: Dictionary containing notification data
        """
        pass

# Concrete Subject - NotificationSubject
class NotificationSubject(Subject):
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self, data: Dict[str, Any]) -> None:
        for observer in self._observers:
            observer.update(data)

# Concrete Observer - UserNotificationObserver
class UserNotificationObserver(Observer):
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def update(self, data: Dict[str, Any]) -> None:
        # Check if this notification is for this user
        if data.get('user_id') == self.user_id:
            from app.models import Notification, db
            
            # Create a new notification in the database
            notification = Notification(
                user_id=self.user_id,
                message=data.get('message', ''),
                read=False
            )
            
            # Add and commit to the database
            db.session.add(notification)
            db.session.commit()

# Global notification subject instance
notification_subject = NotificationSubject()

def get_notification_subject() -> NotificationSubject:
    """
    Get the global notification subject instance
    
    Returns:
        NotificationSubject: The global notification subject
    """
    global notification_subject
    return notification_subject 