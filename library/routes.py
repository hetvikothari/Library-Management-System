from library import app
from .models import Book, Member, Transaction

@app.route("/home")
def home():
    return 'home page'