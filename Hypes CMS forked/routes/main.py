from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from models import db
from models.post import Post
from models.category import Category
from models.comment import Comment
from datetime import datetime
from forms.post import PostForm
from routes.utils import save_picture
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    # Fetch all categories for sidebar filter
    categories = Category.query.all()
    
    # Pagination setup
    page = request.args.get('page', 1, type=int)
    
    # Fetch published posts, ordered by newest first
    posts_pagination = Post.query.filter_by(status='published')\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=5, error_out=False)
        
    return render_template('index.html', 
                           posts=posts_pagination.items, 
                           pagination=posts_pagination,
                           categories=categories,
                           title="Home - Modern CMS")

@main_bp.route('/post/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    # Fetch all categories for sidebar
    categories = Category.query.all()
    
    # Standard query for comments
    comments = post.comments.order_by(Comment.created_at.desc()).all()
    
    return render_template('post_detail.html', 
                           post=post, 
                           comments=comments, 
                           categories=categories, 
                           title=post.title)

@main_bp.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    """AJAX endpoint to submit a comment on a blog post."""
    if not current_user.is_authenticated:
        return jsonify({'error': 'You must be logged in to comment.'}), 401
        
    post = Post.query.filter_by(slug=slug).first()
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
        
    content = request.json.get('content', '').strip()
    if not content:
        return jsonify({'error': 'Comment content cannot be empty.'}), 400
        
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()
    
    # Return details for dynamic frontend injection
    # Render user profile pic source path safely
    profile_pic_url = url_for('static', filename=f'uploads/profiles/{current_user.profile_pic}') if current_user.profile_pic != 'default.png' else url_for('static', filename='uploads/profiles/default.png')
    # Wait, we can define profile pics paths uniformly. Let's make sure it handles both.
    
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'username': current_user.username,
        'profile_pic': profile_pic_url,
        'created_at': comment.created_at.strftime('%b %d, %Y at %I:%M %p')
    }), 200

@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    
    if not query:
        flash('Please enter a search keyword.', 'warning')
        return redirect(url_for('main.home'))
        
    # Search title or content for matches, only published posts
    posts_pagination = Post.query.filter(
        Post.status == 'published',
        (Post.title.like(f'%{query}%')) | (Post.content.like(f'%{query}%'))
    ).order_by(Post.created_at.desc()).paginate(page=page, per_page=5, error_out=False)
    
    return render_template('search.html', 
                           posts=posts_pagination.items, 
                           pagination=posts_pagination,
                           query=query, 
                           categories=categories,
                           title=f"Search Results for '{query}'")

@main_bp.route('/category/<slug>')
def category_posts(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    categories = Category.query.all()
    page = request.args.get('page', 1, type=int)
    
    posts_pagination = Post.query.filter_by(category_id=category.id, status='published')\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=5, error_out=False)
        
    return render_template('category_posts.html', 
                           posts=posts_pagination.items, 
                           pagination=posts_pagination,
                           category=category, 
                           categories=categories,
                           title=f"Category: {category.name}")

@main_bp.route('/about')
def about():
    return render_template('about.html', title='About Us')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # In a real app we'd send an email here.
        # We will simulate successful receipt.
        flash(f'Thank you, {name}! Your message has been sent successfully.', 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html', title='Contact Us')

# Global Error Handlers
@main_bp.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@main_bp.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Server Error'), 500


# --- USER BLOG CREATION & MANAGEMENT ---
@main_bp.route('/blog/write', methods=['GET', 'POST'])
@login_required
def write_post():
    form = PostForm()
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if not categories:
        flash('You must contact an administrator to create a category first.', 'warning')
        return redirect(url_for('main.home'))

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
        flash('Your blog post has been created and published!', 'success')
        return redirect(url_for('main.my_posts'))
        
    return render_template('write_post.html', form=form, legend="Write a Blog Post", title="Write a Blog")


@main_bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Ownership verification
    if post.author != current_user and not current_user.is_admin:
        flash('You do not have permission to edit this post.', 'danger')
        return redirect(url_for('main.home'))
        
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
            post.image_file = save_picture(form.image.data, subfolder='posts')
            
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category_id.data
        post.status = form.status.data
        db.session.commit()
        
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.my_posts'))
        
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category_id.data = post.category_id
        form.status.data = post.status
        
    return render_template('write_post.html', form=form, legend="Edit Post", post=post, title="Edit Post")


@main_bp.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Ownership verification
    if post.author != current_user and not current_user.is_admin:
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('main.home'))
        
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
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.my_posts'))


@main_bp.route('/my-posts')
@login_required
def my_posts():
    # Show user's own posts (both published and drafts)
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
    return render_template('my_posts.html', posts=posts, title="My Blog Posts")
