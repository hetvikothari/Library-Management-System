from library import app, db
from library.models import Book, Member, Transaction
from flask import render_template,redirect,flash,url_for, request

@app.route("/")
@app.route("/home")
def home():
    members = Member.query.order_by(Member.total_fees).all()
    members = members[:10]
    books = Book.query.order_by(Book.total_issue).all()
    books = books[:10]
    return render_template('home.html',members=members, books=books)