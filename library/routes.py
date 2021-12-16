from library import app, db
from library.models import Book, Member, Transaction
from library.forms import AddMember, UpdateMember, AddBook, UpdateBook, AddTransaction
from flask import render_template,redirect,flash,url_for, request
from datetime import date

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/member/add", methods=['GET', 'POST'])
def add_member():
    form = AddMember()
    if form.validate_on_submit():
        member = Member(name=form.name.data, email=form.email.data, debt=0)
        db.session.add(member)
        db.session.commit()
        flash('Member has been added!', 'success')
        return redirect(url_for('view_member'))
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
    if form.validate_on_submit():
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

@app.route("/book/view", methods=['GET'])
def view_book():
    books = Book.query.all()
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

@app.route("/trasaction/", methods=['GET','POST'])
def view_transaction():
    book = Book.query.filter(Book.available_quantity>0).all()
    print(book)
    return render_template('transaction.html', books = book)

@app.route("/book/<int:book_id>/issue", methods=['GET','POST'])
def issue_book(book_id):
    form = AddTransaction()
    if form.validate_on_submit():
        email = form.member_email.data
        member = Member.query.filter_by(email=email).first()
        if(member):
            if(member.debt<=500):
                transaction = Transaction(book_id=book_id, member_id = member.id, issue_date = date.today(), 
                return_date = form.return_date, deadline = form.return_date, fees = 100, status ='issued')
                db.session.add(transaction)
                db.session.commit()
                flash('Book issued successfully','success')
            else:
                flash('Cannot issue book to this member. His debt is greater than 500', 'danger')
        else:
            flash('No such member exsit. Please add member first','danger')
        
    return render_template('add_transaction.html', title='Add Trasanction',
                           form=form, legend='Add Transaction')