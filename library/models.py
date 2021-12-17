from library import db
from datetime import date

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    authors = db.Column(db.String, nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    isbn13 = db.Column(db.Integer, nullable=False)
    language_code = db.Column(db.String(300), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=False)
    text_reviews_count = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    total_quantity = db.Column(db.Integer, default=30)
    available_quantity = db.Column(db.Integer, default=30, nullable=True)
    total_issue = db.Column(db.Integer, default=10, nullable=True)
    transaction = db.relationship('Transaction', backref='book', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.authors}')"

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    debt = db.Column(db.Integer, default=0)
    total_fees = db.Column(db.Integer, default=0)
    transaction = db.relationship('Transaction', backref="member", lazy=True)

    def __repr__(self):
        return f"User('{self.name}')"

    def can_issue(self):
        return self.debt <= 500


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id", ondelete="SET NULL"))
    member_id = db.Column(db.Integer, db.ForeignKey("member.id", ondelete="SET NULL"))
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    deadline = db.Column(db.Date, nullable=False)
    fees = db.Column(db.Integer, default=0)
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.id}')"
