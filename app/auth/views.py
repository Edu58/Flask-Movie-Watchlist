import requests
from flask import render_template, redirect, url_for, request, flash
from . import auth
from .forms import SignUpForm, LoginForm
from flask_login import login_user, login_required, logout_user
from ..models import User
from app import db
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    return render_template('auth/login.html', login=login_form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        send_email("Welcome to watchlist", "email/welcome_user", user.email, user=user)

        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', signup=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
