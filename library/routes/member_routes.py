from library import app, db
from library.models import Book, Member, Transaction
from library.forms import AddMember, UpdateMember, AddBook, UpdateBook, ImportBooks
from flask import render_template,redirect,flash,url_for, request
from datetime import datetime, timedelta
from sqlalchemy import or_

# Add member
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
    return render_template('member/add_member.html', title='Add Member',
                           form=form, legend='Add Member')

# Get all members list
@app.route("/member/view", methods=['GET'])
def view_member():
    members = Member.query.all()
    return render_template('member/member.html', members = members)

# Uodate member data with ID
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
    return render_template('member/add_member.html', title='Update Member',
                           form=form, legend='Update Member')

# Delete member with ID
@app.route("/member/<int:member_id>/delete", methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member has been deleted!', 'success')
    return redirect(url_for('view_member'))