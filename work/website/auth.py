from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user 
from website.forms import ResetRequestForm, ResetPasswordForm
from website import mail
from flask_mail import Message
from flask import current_app

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')


        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 1 character.', category='error')
        elif password != confirm_password:
            flash('Passwords don\'t match', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            new_user = User(email=email, full_name=full_name, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.dashboard'))
        
    return render_template("register.html", user=current_user)

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/about_us')
def about_us():
    return render_template("about_us.html")

def send_mail(user):
    token=user.get_token()
    msg=Message('Password Reset Request', recipients=[user.email], sender='noreply@hohanhdung06.com')
    msg.body=f''' To reset password. Please follow the link below.

    {url_for('auth.reset_token', token=token,_external=True)}
    If you didn't send a password rest request. Please ignore this message

    '''
    mail.send(msg)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form=ResetRequestForm() 
    if request.method == 'POST':
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user: 
                send_mail(user)
            flash('Reset request sent. Check your mail.','success')
    return render_template("forgot_password.html", title='Reset Request', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('That is invalid token or expire. Please try again.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user.password=hashed_password
        db.session.commit()
        flash('Password changed! Please login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('change_password.html', title="Change Password", form=form, token=token) 

@auth.route('/trackWorkout')
def trackWorkout():
    return render_template("trackWorkout2.html")