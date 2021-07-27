# package
from market import app, db
# Flask
from flask import render_template, redirect, url_for, flash, request
# Models
from market.models import Item, User
# Forms
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
# third party
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET': 
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, 
                        email_address=form.email_address.data,
                        password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created succesfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template('signup.html', form=form )

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_password(
                            password_attempted=login_form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are no match! Please try again', category='danger')
            

    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("Yo have been logged out!", category='info')
    return redirect(url_for('home_page'))

@app.route("/about/<username>")
def about_page(username):
    return f'<h2>This is about page of {username}</h2>'