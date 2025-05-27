import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    loginManager.login_view = 'main.login'
    loginManager.login_message_category = 'info'
    migrate.init_app(app, db)

    from app import routes
    app.register_blueprint(routes.bp)

    return app
