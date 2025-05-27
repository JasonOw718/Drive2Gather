from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    db.session.commit()
    print("database initialized")