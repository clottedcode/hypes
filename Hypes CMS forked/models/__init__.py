from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here to make them accessible via models namespace
from models.user import User
from models.post import Post
from models.category import Category
from models.comment import Comment

