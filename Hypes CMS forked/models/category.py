from models import db
from slugify import slugify

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    
    # Relationships
    posts = db.relationship('Post', backref='category', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' in kwargs and not kwargs.get('slug'):
            self.slug = slugify(kwargs['name'])
            
    def __repr__(self):
        return f'<Category {self.name}>'
