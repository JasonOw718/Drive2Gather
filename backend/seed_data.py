from app import create_app
from app.models import db, User, UserRole, Admin, Donor, Passenger, Driver
import os
from werkzeug.security import generate_password_hash

def seed_database():
    print("Seeding database with initial data...")
    
    # Create roles if they don't exist
    roles = ["admin", "donor", "passenger", "driver"]
    existing_roles = UserRole.query.all()
    existing_role_names = [role.role_name for role in existing_roles]
    
    for role in roles:
        if role not in existing_role_names:
            new_role = UserRole(role_name=role)
            db.session.add(new_role)
    
    # Commit roles first
    db.session.commit()
    print("Roles created successfully")
    
    # Create users
    users_data = [
        {
            "name": "Admin User",
            "email": "admin@drive2gather.com",
            "phone": "1234567890",
            "password": generate_password_hash("admin123"),
            "role": "admin"
        },
        {
            "name": "Donor User",
            "email": "donor@drive2gather.com",
            "phone": "2345678901",
            "password": generate_password_hash("donor123"),
            "role": "donor"
        },
        {
            "name": "Passenger User",
            "email": "passenger@drive2gather.com",
            "phone": "3456789012",
            "password": generate_password_hash("passenger123"),
            "role": "passenger"
        },
        {
            "name": "Driver User",
            "email": "driver@drive2gather.com",
            "phone": "4567890123",
            "password": generate_password_hash("driver123"),
            "role": "driver",
            "license_number": "DL12345678",
            "car_number": "CAR1234",
            "car_type": "Sedan",
            "car_color": "Black"
        }
    ]
    
    for user_data in users_data:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            print(f"User {user_data['email']} already exists, skipping...")
            continue
        
        # Create base user
        new_user = User(
            name=user_data["name"],
            email=user_data["email"],
            phone=user_data["phone"],
            password=user_data["password"]
        )
        db.session.add(new_user)
        db.session.flush()  # To get the user_id before commit
        
        # Add role
        role = UserRole(role_name=user_data["role"])
        role.user_id = new_user.user_id
        db.session.add(role)
        
        # Add role-specific details
        if user_data["role"] == "admin":
            admin = Admin(user_id=new_user.user_id)
            db.session.add(admin)
        elif user_data["role"] == "donor":
            donor = Donor(user_id=new_user.user_id)
            db.session.add(donor)
        elif user_data["role"] == "passenger":
            passenger = Passenger(user_id=new_user.user_id)
            db.session.add(passenger)
        elif user_data["role"] == "driver":
            driver = Driver(
                user_id=new_user.user_id,
                license_number=user_data["license_number"],
                car_number=user_data["car_number"],
                car_type=user_data["car_type"],
                car_color=user_data["car_color"]
            )
            db.session.add(driver)
    
    # Commit all users
    db.session.commit()
    print("Users created successfully")
    
    print("Database seeding completed!")

if __name__ == "__main__":
    app = create_app()
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    with app.app_context():
        seed_database() 