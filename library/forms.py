from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email
from library.models import Member,Book,Transaction


class AddMember(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add')

class UpdateMember(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Member')

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

class ImportBooks(FlaskForm):
    number_of_books = IntegerField("Number of books to import",validators=[DataRequired()])
    title = StringField("Book title")
    authors = StringField("Book Authors")
    submit = SubmitField('Import Book')
