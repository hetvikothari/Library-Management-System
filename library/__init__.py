from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba156'

ENV = 'dev'
if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from library.routes import routes, book_routes, member_routes, transaction_routes 