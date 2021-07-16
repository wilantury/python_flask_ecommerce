# flask
from flask import Flask
# third party
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '3fb6498c3bf54d4b3e1d04f0'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# routes
from market import routes