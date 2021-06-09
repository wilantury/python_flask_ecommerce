# package
from market import app
# Flask
from flask import render_template
# Models
from market.models import Item


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route("/about/<username>")
def about_page(username):
    return f'<h2>This is about page of {username}</h2>'