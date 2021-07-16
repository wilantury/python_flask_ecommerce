# package
from market import app, db
# Flask
from flask import render_template, redirect, url_for, flash
# Models
from market.models import Item, User
# Forms
from market.forms import RegisterForm

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                        email_address=form.email_address.data,
                        password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template('signup.html', form=form )

@app.route("/about/<username>")
def about_page(username):
    return f'<h2>This is about page of {username}</h2>'