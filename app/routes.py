from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Product


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/store')
def store():
    products = db.session.scalars(sa.select(Product)).all()
    return render_template('store.html', title='Store', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add-to-basket', methods=['POST'])
def add_to_basket():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract item ID from the received data
        item_id = data.get('id')
        
        if not item_id:
            return jsonify({'message': 'Item ID is missing!'}), 400
        

        return jsonify({'message': 'Item added to basket!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
