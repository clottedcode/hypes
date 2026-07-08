import os

class Config:
    # Secret key for session signing and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-college-project-cms-1823912'
    
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # SQLite Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'cms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder configuration
    # Uploads are stored in static/uploads so they are served directly by the web server
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    # Max image upload size: 5MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    
    # Allowed file extensions for image uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
