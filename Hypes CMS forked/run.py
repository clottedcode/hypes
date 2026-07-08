import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from models.category import Category
from models.post import Post
from routes import auth_bp, main_bp, admin_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    
    # Setup Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Ensure instance / upload folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'posts'), exist_ok=True)
    
    # Automatic DB creation & seeding
    with app.app_context():
        db.create_all()
        seed_database()
        
    return app

def seed_database():
    """Seeds default categories and an admin account if database is empty."""
    # Seed Categories
    if Category.query.first() is None:
        tech = Category(name="Technology", description="Gadgets, computers, tutorials, software, and programming updates.")
        edu = Category(name="Education", description="Academic resources, studies advice, learning strategies, and tips.")
        life = Category(name="Lifestyle", description="Fitness, health, travels, diets, reviews, and daily vlogs.")
        sci = Category(name="Science", description="Discoveries, outer space, innovations, climate, and engineering fields.")
        
        db.session.add_all([tech, edu, life, sci])
        db.session.commit()
        print("[Database Seed] Categories seeded successfully.")
        
    # Seed Admin User
    if User.query.filter_by(role='admin').first() is None:
        admin = User(
            username="admin", 
            email="admin@cms.com", 
            role="admin", 
            profile_pic="default.png"
        )
        admin.set_password("admin123")  # Clear default password for testing
        db.session.add(admin)
        db.session.commit()
        print("[Database Seed] Admin user created (Username: admin, Password: admin123).")
        
        # Optionally add a sample seed post
        if Post.query.first() is None:
            tech_cat = Category.query.filter_by(name="Technology").first()
            sample_post = Post(
                title="Exploring Python Flask MVC for Web Development",
                content="""<p>Python Flask is a powerful, lightweight microframework that excels at building modular, clean web applications. When coupled with an MVC (Model-View-Controller) folder structure, Flask helps developers segregate data access logic from layout templates and endpoint routes efficiently.</p>
                <p>In this dynamic CMS project, we utilize SQLAlchemy as an Object-Relational Mapper (ORM) targeting an SQLite database engine. By adopting modular Jinja2 layout templates, WTForms for data validations, and secure Werkzeug password hashes, we show a highly robust and state-of-the-art final year project layout.</p>
                <h5>Key features highlighted:</h5>
                <ul>
                    <li>Dynamic SEO Friendly URL Slugs</li>
                    <li>Secure Session tracking and password hashes</li>
                    <li>Admin overview analytics graphics</li>
                    <li>Live comment updates with AJAX</li>
                </ul>""",
                status="published",
                image_file="default_post.jpg",  # Uses the beautiful tech banner generated earlier
                author=admin,
                category=tech_cat
            )
            db.session.add(sample_post)
            db.session.commit()
            print("[Database Seed] Sample starter post seeded successfully.")

app = create_app()

if __name__ == '__main__':
    # Boot development server
    app.run(debug=True, host='127.0.0.1', port=5000)
