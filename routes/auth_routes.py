from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        next_url = request.args.get("next")
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(next_url or url_for('home'))
        else:
            flash('Invalid credentials, try again.')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'patient').strip().lower()
        specialization = request.form.get('specialization', '').strip()

        if role not in {'patient', 'doctor', 'lab_expert'}:
            flash('Please choose a valid account role.')
            return render_template('register.html')

        if not username or not email or not password:
            flash('All fields are required.')
            return render_template('register.html')

        if confirm_password and password != confirm_password:
            flash('Passwords do not match.')
            return render_template('register.html')

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('A user with that email or username already exists.')
        else:
            new_user = User(
                username=username,
                email=email,
                role=role,
                specialization=specialization or None,
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.')
            return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
