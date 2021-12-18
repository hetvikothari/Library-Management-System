from library import app, db
from library.models import Book, Member, Transaction
from library.forms import AddMember, UpdateMember, AddBook, UpdateBook, ImportBooks
from flask import render_template,redirect,flash,url_for, request
from datetime import datetime, timedelta
from sqlalchemy import or_
import math
import requests

#add new book
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
    return render_template('book/add_book.html', title='Add Book',
                           form=form, legend='Add Book')

# view all books 
@app.route("/book/view", methods=['GET','POST'])
def view_book():
    books = Book.query.all()
    if request.method == "POST":
       keyword = request.form.get("text")
       books = Book.query.filter(or_(Book.title.ilike('%{}%'.format(keyword)), Book.authors.ilike('%{}%'.format(keyword)))).all() 
       if books is not None:
            return render_template("book/book.html", books=books)
       else:
           flash('No such books exist.','Danger')
    return render_template('book/book.html', books=books)

# delete a book with ID
@app.route("/book/<int:book_id>/delete", methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted!', 'success')
    return redirect(url_for('view_book'))

# update book with ID
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
    return render_template('book/add_book.html', title='Update Book',
                           form=form, legend='Update Book')

# import books from Frappe API
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

    return render_template("book/import_book.html", form=form, title='Import Book',  legend='Import Book')
