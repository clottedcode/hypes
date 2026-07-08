from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Images only!')])
    status = SelectField('Status', choices=[('published', 'Published'), ('draft', 'Draft')], default='published')
    submit = SubmitField('Save Post')
