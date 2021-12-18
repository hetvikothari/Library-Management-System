from library import app, db
from library.models import Book, Member, Transaction
from flask import render_template,redirect,flash,url_for, request
from datetime import datetime, timedelta
from sqlalchemy import or_
import math
import requests

# View all transactions
@app.route("/transactions/view", methods=['GET','POST'])
def view_transaction():
    transactions = Transaction.query.all()
    for transaction in transactions:
        member= Member.query.filter_by(id=transaction.member_id).first()
        if member is not None:
            transaction.member_name = member.name
        book = Book.query.filter_by(id=transaction.book_id).first()
        if book is not None:
            transaction.book_name = book.title
    return render_template('transaction/view_transaction.html', transactions=transactions)

# Show books that are available
@app.route("/transaction/", methods=['GET','POST'])
def add_transaction():
    book = Book.query.filter(Book.available_quantity > 0).all()
    if request.method == "POST":
       keyword = request.form.get("text")
       books = Book.query.filter(or_(Book.title.ilike('%{}%'.format(keyword)), Book.authors.ilike('%{}%'.format(keyword)))).all() 
       for book in books:
           if(book.available_quantity<=0):
               books.remove(book)
       if books is not None:
            return render_template("transaction/add_transaction.html", books=books)
       else:
           flash('No such books exist.','Danger')
    return render_template('transaction/add_transaction.html', books = book)

# Issue Book
@app.route("/book/<int:book_id>/issue", methods=['GET','POST'])
def issue_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST' :
        if(book.available_quantity <= 0):
            flash('Book not available','danger')
            return redirect(url_for('add_transaction'))
        email = request.form.get('email')
        member = Member.query.filter_by(email=email).first()
        if(member):
            if(member.debt<=500):
                return_date = datetime.today()+timedelta(days=30)
                transaction = Transaction(book_id=book_id, member_id = member.id, issue_date = datetime.today(), 
                return_date = return_date, deadline = return_date, fees = 100, status ='issued')
                book = Book.query.get_or_404(book_id)
                book.total_issue = book.total_issue + 1
                book.available_quantity = book.available_quantity - 1
                db.session.add(transaction)
                db.session.commit()                         
                flash('Book issued successfully','success')
                return redirect(url_for('view_transaction'))
            else:
                flash('Cannot issue book to this member. His debt is greater than 500', 'danger')
                return redirect(url_for('view_transaction'))
        else:
            flash('No such member exsit. Please add member first','danger')
            return redirect(url_for('home'))
    return redirect(url_for('view_transaction'))

# return book
@app.route("/book/<int:transaction_id>/return", methods=['GET','POST'])
def return_book(transaction_id):
    transactions = Transaction.query.get_or_404(transaction_id)
    member_id = transactions.member_id
    book_id = transactions.book_id
    member = Member.query.get_or_404(member_id)
    book = Book.query.get_or_404(book_id)
    book.available_quantity = book.available_quantity + 1
    paid = request.form.get('paid')
    if(paid):
        member.total_fees = member.total_fees + 100
        member.debt = member.debt - 100
    else:
        member.debt = member.debt + 100
    transaction = Transaction(book_id=book_id, member_id = member.id, issue_date = transactions.issue_date, 
                return_date = datetime.today(), deadline = transactions.deadline, fees = 100, status ='returned')
    db.session.delete(transactions)
    db.session.commit() 
    db.session.add(transaction)
    db.session.commit()
    flash('Book returned sucessfully','success')
    book = Book.query.filter(Book.available_quantity > 0).all()
    return redirect(url_for('view_transaction'))