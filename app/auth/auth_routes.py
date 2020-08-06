from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from app import db
from app.auth.auth_forms import LoginForm, RegistrationForm
from app.models import Users

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('golf.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('golf.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route("/logout", methods=["POST","GET"])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('golf.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(
            team_name=form.team_name.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
            points=0
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)