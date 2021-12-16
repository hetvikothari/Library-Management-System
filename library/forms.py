from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, FloatField
from wtforms.validators import DataRequired, Email
from library.models import Member,Book,Transaction


class AddMember(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Add')

class UpdateMember(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddBook(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Author', validators=[DataRequired()])
    average_rating = FloatField('Average Rating', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    isbn13 = StringField('ISBN13', validators=[DataRequired()])
    language_code = StringField('Language Code', validators=[DataRequired()])
    num_pages = IntegerField('Pages', validators=[DataRequired()])
    ratings_count = IntegerField('Ratings Count', validators=[DataRequired()])
    text_reviews_count = IntegerField('Text Count', validators=[DataRequired()])
    publication_date = DateField('Publication Date', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    total_quantity = IntegerField('Total Quantity', validators=[DataRequired()])
    available_quantity = IntegerField('Available Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class UpdateBook(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Author', validators=[DataRequired()])
    average_rating = FloatField('Average Rating', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    isbn13 = StringField('ISBN13', validators=[DataRequired()])
    language_code = StringField('Language Code', validators=[DataRequired()])
    num_pages = IntegerField('Pages', validators=[DataRequired()])
    ratings_count = IntegerField('Ratings Count', validators=[DataRequired()])
    text_reviews_count = IntegerField('Text Count', validators=[DataRequired()])
    publication_date = DateField('Publication Date', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    total_quantity = IntegerField('Total Quantity', validators=[DataRequired()])
    available_quantity = IntegerField('Available Quantity')
    submit = SubmitField('Update')

class AddTransaction(FlaskForm):
    member_email = StringField('Member Email', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()], format='%m/%d/%Y')
    submit = SubmitField('Add Transaction')
