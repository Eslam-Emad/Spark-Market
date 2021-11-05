from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from market import app, db
from market.forms.login import LoginForm
from market.forms.purchase_item import PurchaseItemForm
from market.forms.register import RegisterForm
from market.forms.sell_item import SellItemForm
from market.models.item import Item
from market.models.user import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item
        purchased_item = request.form.get('purchase_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                # buy
                purchased_item_object.assign_ownership(current_user)
                flash("Congrats your purchases done", category='success')
            else:
                flash(f"Your budget not allowing you to buy {purchased_item_object.name}", category='danger')
        # Sell Item
        sell_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sell_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                # sell
                sold_item_object.remove_ownership(current_user)
                flash("item has been removed", category='danger')
            else:
                flash(f"Something went wrong with selling {sold_item_object.name}", category='danger')
        return redirect(url_for("market_page"))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=sell_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email_address.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Your account has been created", category='success')
        return redirect(url_for('home'))
    if form.errors != {}:
        for msg in form.errors.values():
            flash(f'{msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email_address.data).first()
        if user and user.validate_password(form.password.data):
            login_user(user)
            flash(f"{user.username} You logged in successfully", category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'email or password is wrong', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash(f"You have beet logged out", category='info')
    return redirect(url_for("login_page"))
