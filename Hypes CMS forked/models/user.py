from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    profile_pic = db.Column(db.String(120), nullable=False, default='default.png')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Verifies password hashes."""
        return check_password_hash(self.password_hash, password)
        
    @property
    def is_admin(self):
        """Helper to quickly check user privilege level."""
        return self.role == 'admin'
        
    def __repr__(self):
        return f'<User {self.username}>'
