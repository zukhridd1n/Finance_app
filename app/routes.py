from flask import render_template, flash, redirect, url_for, request, session
from app import db,app,bcrypt
from app.decarators import login_required
from app.forms import RegistrationForm, LoginForm, DeleteAccountForm, AddBalancesForm
from app.models import User_Details, Balance


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
@login_required(required=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User_Details.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome {user.username}", "success")
            return redirect(url_for("home"))
        else:
            flash("username or password wrong", "danger")

    return render_template('auth/login.html', form=form)


@app.route("/register", methods=["POST", "GET"])
@login_required(required=False)
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        confirm_password_hesh = bcrypt.generate_password_hash(form.confirm_password.data).decode("utf-8")
        user = User_Details(username=form.username.data, password=hashed_password, email=form.email.data,
                            phone=form.phone.data, confirm_password=confirm_password_hesh)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("auth/register.html",form=form)


@app.route("/add_balance", methods=["POST", "GET"])
@login_required(required=True)
def add_balance():
    user_id = session.get('user_id')
    form = AddBalancesForm()
    if form.validate_on_submit():
        amount = form.amount.data
        user = User_Details.query.filter_by(id=user_id).first()
        user_balance = Balance.query.filter_by(user_id=user.id).first()
        if user_balance:
            user_balance.amount += float(amount)
        else:
            balance = Balance(amount=float(amount), user_id=user.id)
            db.session.add(balance)
        db.session.commit()
        flash('Add balance successfully', 'success')
        return redirect(url_for('home'))
    return render_template('blogs/add-balance.html', form=form)


@app.route("/delete_account", methods=["POST", "GET"])
@login_required(required=True)
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = User_Details.query.filter_by(id=session.get('user_id'), username=form.username.data, phone=form.phone.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            user.is_deleted = True
            db.session.commit()
            session.pop('username')
            flash('You deleted account.But you can recover the account again.', 'info')
            return redirect(url_for('home'))
        else:
            flash('username or password is wrong!', 'danger')
    return render_template('blogs/delete-account.html', form=form)


@app.route("/show_balance", methods=["POST", "GET"])
@login_required(required=True)
def show_balance():
    user_id = session.get('user_id')
    balance = Balance.query.filter_by(user_id=user_id).first()
    return render_template('blogs/show-balance.html', balance=balance)


@app.route("/transfer_history", methods=["POST", "GET"])
@login_required(required=True)
def transfer_history():
    return render_template("blogs/transfer-history.html")


@app.route("/transfer_money", methods=["POST", "GET"])
@login_required(required=True)
def transfer_money():
    return render_template("blogs/transfer-money.html")


@app.route("/log_out")
@login_required(required=True)
def log_out():
    session.pop("user_id")
    username = session.pop("username")
    flash(f"{username} user successfully loged out", "info")
    return redirect(url_for("home"))


@app.route("/profile_info", methods=["POST", "GET"])
@login_required(required=True)
def profile_info():
    user = User_Details.query.filter_by(id=session.get('user_id')).first()
    return render_template('blogs/profile.html', user=user)