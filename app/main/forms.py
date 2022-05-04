from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    title = StringField('Movie title', validators=[DataRequired()])
    review = TextAreaField('Your review')
    submit = SubmitField('Submit')


class Updateprofile(FlaskForm):
    bio = StringField('About You', validators=[DataRequired()])
    submit = SubmitField('Submit')
