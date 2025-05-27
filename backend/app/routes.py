import os
import secrets
from sqlalchemy import or_
from flask import render_template, url_for, redirect, flash, request, abort, session, Blueprint, jsonify
from flask import current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db, bcrypt
from app.forms import (RegistrationForm, LoginForm)
from app.models import User

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    return render_template('home.html')

@bp.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('regis.html', title='Register', form=form)

@bp.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else :
            flash("Login unsuccessful. Please check your username and password again.", 'danger')
    return render_template('login.html', title='Login', form = form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
