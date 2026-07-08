from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from models import db
from models.user import User
from models.post import Post
from models.category import Category
from models.comment import Comment
from forms.post import PostForm
from forms.category import CategoryForm
from routes.utils import save_picture
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def restrict_to_admins():
    """Ensure that only users with the 'admin' role can access admin endpoints."""
    if not current_user.is_admin:
        flash('Access denied. Administrative privileges are required.', 'danger')
        return redirect(url_for('main.home'))

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard landing page. Compiles counts and graph analytics."""
    # Compilation of metrics cards
    total_posts = Post.query.count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    total_comments = Comment.query.count()
    
    published_posts = Post.query.filter_by(status='published').count()
    draft_posts = Post.query.filter_by(status='draft').count()
    
    # Calculate category distributions for Chart.js
    categories = Category.query.all()
    chart_labels = []
    chart_data = []
    for cat in categories:
        chart_labels.append(cat.name)
        chart_data.append(cat.posts.count())
        
    # Standard SQLite post creation counts over last 5 posts to display in table
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                           title="Admin Dashboard",
                           total_posts=total_posts,
                           total_categories=total_categories,
                           total_users=total_users,
                           total_comments=total_comments,
                           published_posts=published_posts,
                           draft_posts=draft_posts,
                           chart_labels=chart_labels,
                           chart_data=chart_data,
                           recent_posts=recent_posts,
                           recent_users=recent_users)

# --- POSTS CRUD ---
@admin_bp.route('/posts')
def list_posts():
    """Displays a list of all posts in a table for administrative tasks."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('dashboard/posts.html', posts=posts, title="Manage Posts")

@admin_bp.route('/post/new', methods=['GET', 'POST'])
def create_post():
    """Renders post creation form and handles saves."""
    form = PostForm()
    # Dynamically populate categories dropdown
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if not categories:
        flash('You must create a category before publishing a post.', 'warning')
        return redirect(url_for('admin.create_category'))

    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = save_picture(form.image.data, subfolder='posts')
            
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category_id.data,
            status=form.status.data,
            image_file=image_file,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin.list_posts'))
        
    return render_template('dashboard/post_form.html', form=form, legend="New Post", title="Create Post")

@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Renders editing form for a post and saves modifications."""
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        if form.image.data:
            # Delete old image if it exists and wasn't default
            if post.image_file and post.image_file != 'default_post.jpg':
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', post.image_file)
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception:
                        pass
            # Save new image
            post.image_file = save_picture(form.image.data, subfolder='posts')
            
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category_id.data
        post.status = form.status.data
        db.session.commit()
        
        flash('Post has been updated!', 'success')
        return redirect(url_for('admin.list_posts'))
        
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category_id.data = post.category_id
        form.status.data = post.status
        
    return render_template('dashboard/post_form.html', form=form, legend="Edit Post", post=post, title="Edit Post")

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Secure POST endpoint to delete an existing post."""
    post = Post.query.get_or_404(post_id)
    
    # Delete uploaded image
    if post.image_file and post.image_file != 'default_post.jpg':
        img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', post.image_file)
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
            except Exception:
                pass
                
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.list_posts'))

# --- CATEGORIES CRUD ---
@admin_bp.route('/categories')
def list_categories():
    """Displays all categories for administration."""
    categories = Category.query.all()
    return render_template('dashboard/categories.html', categories=categories, title="Manage Categories")

@admin_bp.route('/category/new', methods=['GET', 'POST'])
def create_category():
    """Renders category creation forms."""
    form = CategoryForm()
    if form.validate_on_submit():
        # Check duplicate category name
        existing = Category.query.filter_by(name=form.name.data).first()
        if existing:
            flash('Category name already exists.', 'danger')
            return render_template('dashboard/category_form.html', form=form, legend="New Category", title="Create Category")
            
        category = Category(name=form.name.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.list_categories'))
        
    return render_template('dashboard/category_form.html', form=form, legend="New Category", title="Create Category")

@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    """Renders edit category screen and applies changes."""
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        # Check name collisions
        existing = Category.query.filter(Category.name == form.name.data, Category.id != category_id).first()
        if existing:
            flash('Category name already exists.', 'danger')
            return render_template('dashboard/category_form.html', form=form, legend="Edit Category", title="Edit Category")
            
        category.name = form.name.data
        category.description = form.description.data
        # Recalculate slug
        from slugify import slugify
        category.slug = slugify(category.name)
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.list_categories'))
        
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
        
    return render_template('dashboard/category_form.html', form=form, legend="Edit Category", title="Edit Category")

@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """Secure endpoint to remove a category."""
    category = Category.query.get_or_404(category_id)
    
    # Dissociate or delete posts under this category?
    # According to post schema category_id SET NULL is handled by DB cascade, let's execute standard deletion.
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.list_categories'))

# --- USER MANAGEMENT ---
@admin_bp.route('/users')
def list_users():
    """Displays a list of registered users for administrative view."""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard/users.html', users=users, title="Manage Users")
