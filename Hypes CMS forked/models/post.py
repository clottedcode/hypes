from datetime import datetime
from models import db
from slugify import slugify

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(100), nullable=True)  # Store image name in static/uploads
    status = db.Column(db.String(20), nullable=False, default='published')  # 'published' or 'draft'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'title' in kwargs and not kwargs.get('slug'):
            self.slug = self.generate_unique_slug(kwargs['title'])
            
    def generate_unique_slug(self, title):
        """Generates a unique slug by appending numbers if slug already exists."""
        base_slug = slugify(title)
        unique_slug = base_slug
        counter = 1
        # Check database for collision
        while Post.query.filter_by(slug=unique_slug).first() is not None:
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        return unique_slug

    def __repr__(self):
        return f'<Post {self.title}>'
