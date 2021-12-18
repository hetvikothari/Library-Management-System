from library import app, db
from library.models import Book, Member, Transaction
from library.forms import AddMember, UpdateMember, AddBook, UpdateBook, ImportBooks
from flask import render_template,redirect,flash,url_for, request
from datetime import datetime, timedelta
from sqlalchemy import or_
import math
import requests

@app.route("/")
@app.route("/home")
def home():
    members = Member.query.order_by(Member.total_fees).all()
    members = members[:10]
    books = Book.query.order_by(Book.total_issue).all()
    books = books[:10]
    return render_template('home.html',members=members, books=books)

@app.route("/member/add", methods=['GET', 'POST'])
def add_member():
    form = AddMember()
    if form.validate_on_submit() and request.method == "POST":
        member = Member(name=form.name.data, email=form.email.data, debt=0)
        db.session.add(member)
        db.session.commit()
        flash('Member has been added!', 'success')
        return redirect(url_for('view_member'))
    else:
        print(form.errors)
    return render_template('add_member.html', title='Add Member',
                           form=form, legend='Add Member')

@app.route("/member/view", methods=['GET'])
def view_member():
    members = Member.query.all()
    return render_template('member.html', members = members)

@app.route("/member/<int:member_id>/update", methods=['GET', 'POST'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    form = UpdateMember()
    if form.validate_on_submit() and request.method == "POST":
        member.name = form.name.data
        member.email = form.email.data
        db.session.commit()
        flash('Member details have been updated!', 'success')
        return redirect(url_for('view_member'))
    elif request.method == 'GET':
        form.name.data = member.name
        form.email.data = member.email
    return render_template('add_member.html', title='Update Member',
                           form=form, legend='Update Member')

@app.route("/member/<int:member_id>/delete", methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member has been deleted!', 'success')
    return redirect(url_for('view_member'))

@app.route("/book/add", methods=['GET', 'POST'])
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        book = Book(title=form.title.data, authors=form.authors.data, 
        average_rating=form.average_rating.data, isbn = form.isbn.data, 
        isbn13=form.isbn13.data, language_code = form.language_code.data, 
        num_pages = form.num_pages.data, ratings_count = form.ratings_count.data, 
        text_reviews_count=form.text_reviews_count.data, publication_date = form.publication_date.data, 
        publisher = form.publisher.data, total_quantity = form.total_quantity.data)
        db.session.add(book)
        db.session.commit()
        flash('Book has been added!', 'success')
        return redirect(url_for('view_book'))
    return render_template('add_book.html', title='Add Book',
                           form=form, legend='Add Book')

@app.route("/book/view", methods=['GET','POST'])
def view_book():
    books = Book.query.all()
    if request.method == "POST":
       keyword = request.form.get("text")
       books = Book.query.filter(or_(Book.title.ilike('%{}%'.format(keyword)), Book.authors.ilike('%{}%'.format(keyword)))).all() 
    #    print(books)
       return render_template("book.html", books=books)
    return render_template('book.html', books=books)


@app.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted!', 'success')
    return redirect(url_for('view_book'))

@app.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = UpdateBook()
    if form.validate_on_submit():
        book.title = form.title.data
        book.authors = form.authors.data
        book.average_rating = form.average_rating.data
        book.isbn = form.isbn.data
        book.isbn13 = form.isbn13.data
        book.language_code = form.language_code.data
        book.num_pages = form.num_pages.data
        book.ratings_count = form.ratings_count.data
        book.text_reviews_count = form.text_reviews_count.data
        book.publication_date = form.publication_date.data
        book.publisher = form.publisher.data
        book.total_quantity = form.total_quantity.data
        book.available_quantity = form.available_quantity.data
        db.session.commit()
        flash('Book details have been updated!', 'success')
        return redirect(url_for('view_book'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.authors.data = book.authors
        form.average_rating.data = book.average_rating
        form.isbn.data = book.isbn
        form.isbn13.data = book.isbn13
        form.language_code.data = book.language_code
        form.num_pages.data = book.num_pages
        form.ratings_count.data = book.ratings_count
        form.text_reviews_count.data = book.text_reviews_count
        form.publication_date.data = book.publication_date
        form.publisher.data = book.publisher
        form.total_quantity.data = book.total_quantity 
        form.available_quantity.data = book.available_quantity       
    return render_template('add_book.html', title='Update Book',
                           form=form, legend='Update Book')

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
    return render_template('view_transaction.html', transactions=transactions)

@app.route("/transaction/", methods=['GET','POST'])
def add_transaction():
    book = Book.query.filter(Book.available_quantity > 0).all()
    return render_template('add_transaction.html', books = book)


@app.route("/book/<int:book_id>/issue", methods=['GET','POST'])
def issue_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST' :
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

@app.route("/book/import", methods=["GET", "POST"])
def import_book():
    form = ImportBooks()
    if request.method == "POST":
        pages = math.ceil(form.number_of_books.data / 20)
        count = 0

        for i in range(pages):
            url = f"https://frappe.io/api/method/frappe-library/?page={i+1}"
            payload = {"page": i + 1}
            if form.title.data:
                payload["title"] = form.title.data
            if form.authors.data:
                payload["authors"] = form.authors.data
            response = requests.get(url, params=payload)

            if response.status_code != 200:
                break
            response = response.json()
            if not response["message"] or count == form.number_of_books.data:
                break
            for book in response["message"]:
                if count == form.number_of_books.data:
                    break

                new_book = Book(
                    title=book["title"],
                    authors=book["authors"],
                    average_rating=float(book["average_rating"]),
                    language_code=book["language_code"],
                    num_pages=book["  num_pages"],
                    ratings_count=int(book["ratings_count"]),
                    text_reviews_count=int(book["text_reviews_count"]),
                    publication_date=datetime.strptime(book["publication_date"], "%m/%d/%Y"),
                    publisher=book["publisher"],
                    isbn=book["isbn"],
                    isbn13=book["isbn13"],
                    total_quantity=30,
                    available_quantity=30,
                    total_issue=0,
                )
                db.session.add(new_book)
                count += 1

        flash(f"Books successfully imported!", category="success")
        db.session.commit()

    return render_template("import_book.html", form=form)
