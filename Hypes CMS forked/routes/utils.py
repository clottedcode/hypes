import os
import uuid
from flask import current_app

def save_picture(form_picture, subfolder=''):
    """Saves an uploaded image to the static uploads directory with a unique filename."""
    # Generate unique filename
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = uuid.uuid4().hex + f_ext
    
    # Determine absolute path to save
    upload_path = current_app.config['UPLOAD_FOLDER']
    if subfolder:
        upload_path = os.path.join(upload_path, subfolder)
        
    # Ensure directories exist
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    picture_path = os.path.join(upload_path, picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn
