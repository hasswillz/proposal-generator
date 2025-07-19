# app/auth/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user
from app.auth.forms import LoginForm, RegistrationForm
from app.auth import auth_bp
from app.models import User
from app import db


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if request.is_json:
            return jsonify({'redirect': url_for('main.dashboard')})
        return redirect(url_for('main.dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)

            if request.is_json:
                return jsonify({
                    'status': 'success',
                    'redirect': url_for('main.dashboard')
                })

            return redirect(url_for('main.dashboard'))

        # Failed login
        if request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401

        flash('Invalid email or password', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash('Registration successful!', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.dashboard'))