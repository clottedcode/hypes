from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import db
from models.user import User
from forms.auth import RegistrationForm, LoginForm, ProfileForm
from routes.utils import save_picture

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Grant admin privilege automatically if the username or email contains "admin" (ideal for local testing)
        if 'admin' in form.username.data.lower() or 'admin' in form.email.data.lower():
            user.role = 'admin'
            
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            
            # If admin, redirect to admin dashboard; else go home or next page
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(original_username=current_user.username, original_email=current_user.email)
    
    if form.validate_on_submit():
        if form.profile_pic.data:
            # Save profile pic to static/uploads/profiles
            picture_file = save_picture(form.profile_pic.data, subfolder='profiles')
            current_user.profile_pic = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    return render_template('profile.html', title='Profile', form=form)
