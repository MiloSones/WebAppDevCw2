import stripe
from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, jsonify, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Product, Basket


stripe.api_key = "sk_test_51QS74ZFYg0cFbH8aJY0YtdeO3lQWEFotcyKMTdxrRo9xJ3YQk523nJmgAWGRdnRPhVzlwaXNt4oaEEHMEPSoWLrh00FLRLYt6i"

@app.route('/')
@app.route('/index')
def index():
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



@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = db.session.scalar(
        sa.select(Product).where(Product.id == product_id)
    )
    if not product:
        flash("Product not found!")
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)



@app.route('/basket')
@login_required
def basket():
    basket_entries = db.session.scalars(
        sa.select(Basket).where(Basket.user_id == current_user.id)
    ).all()

    basket_items = []
    total_price = 0
    total_items = 0

    for entry in basket_entries:
        product = db.session.scalar(
            sa.select(Product).where(Product.id == entry.product_id)
        )
        if product:
            basket_items.append({
                'id': entry.id,
                'title': product.title,
                'category': product.category,
                'price': product.price,
                'quantity': entry.quantity,
                'stock': product.stock,
                'total': round(product.price * entry.quantity, 2)
            })
            total_price += product.price * entry.quantity
            total_items += entry.quantity

    return render_template(
        'basket.html',
        basket_items=basket_items,
        total_price=round(total_price, 2),
        total_items=total_items,
    )

@app.route('/add-to-basket', methods=['POST'])
@login_required
def add_to_basket():
    try:
        item_id = request.form.get('id')

        if not item_id:
            flash('Item ID is missing!')
            return redirect(url_for('index'))

        product = db.session.scalar(
            sa.select(Product).where(Product.id == int(item_id))
        )

        if not product:
            flash('Product not found!')
            return redirect(url_for('index'))

        existing_item = db.session.scalar(
            sa.select(Basket).where(Basket.user_id == current_user.id, Basket.product_id == product.id)
        )

        if existing_item:
            existing_item.quantity += 1
        else:
            new_basket_item = Basket(
                user_id=current_user.id,
                product_id=product.id,
                quantity=1
            )
            db.session.add(new_basket_item)

        db.session.commit()
        flash(f'Added {product.title} to your basket.')

        return redirect(url_for('product_detail', product_id=product.id))

    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the item to the basket.')
        if request.is_json:
            return jsonify({'message': str(e)}), 500
        return redirect(url_for('index'))

@app.route('/remove-from-basket', methods=['POST'])
@login_required
def remove_from_basket():
    try:
        data = request.get_json()
        basket_item_id = data.get('id')

        if not basket_item_id:
            return jsonify({'success': False, 'message': 'Basket item ID is missing!'}), 400

        basket_item = db.session.scalar(
            sa.select(Basket).where(
                Basket.id == basket_item_id,
                Basket.user_id == current_user.id
            )
        )

        if not basket_item:
            return jsonify({'success': False, 'message': 'Basket item not found!'}), 404

        db.session.delete(basket_item)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Item removed from basket.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.'}), 500


@app.route('/update-basket-quantity', methods=['POST'])
@login_required
def update_basket_quantity():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        new_quantity = data.get('quantity')

        if not item_id or not new_quantity:
            return jsonify({'success': False, 'message': 'Item ID or quantity is missing!'}), 400

        new_quantity = int(new_quantity)
        if new_quantity < 1:
            return jsonify({'success': False, 'message': 'Quantity must be at least 1.'}), 400

        basket_item = db.session.scalar(
            sa.select(Basket).where(Basket.id == int(item_id), Basket.user_id == current_user.id)
        )

        if not basket_item:
            return jsonify({'success': False, 'message': 'Basket item not found!'}), 404

        basket_item.quantity = new_quantity
        db.session.commit()

        return jsonify({'success': True, 'message': 'Quantity updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.context_processor
def inject_basket_count():
    total_items = 0
    if current_user.is_authenticated:
        basket_entries = db.session.scalars(
            sa.select(Basket).where(Basket.user_id == current_user.id)
        ).all()
        total_items = sum(entry.quantity for entry in basket_entries)
    return {'total_items': total_items}


@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        basket_items = db.session.scalars(sa.select(Basket).where(Basket.user_id == current_user.id))
        line_items = []

        for item in basket_items:
            product = db.session.scalar(sa.select(Product).where(Product.id == item.product_id))
            if product:
                if item.quantity > product.stock:
                    flash(f"Insufficient stock for {product.title}. Please adjust your basket.")
                    return redirect(url_for('basket'))
                line_items.append({
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': product.title,
                            'description': product.description,
                        },
                        'unit_amount': int(product.price * 100),  # Stripe expects prices in cents
                    },
                    'quantity': item.quantity,
                })

        if not line_items:
            flash("Your basket is empty.")
            return redirect(url_for('basket'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('checkout_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('basket', _external=True),
        )

        # Redirect to Stripe's hosted checkout page
        return redirect(session.url)

    except Exception as e:
        flash(f"An error occurred during checkout: {str(e)}")
        return redirect(url_for('basket'))

@app.route('/checkout/success', methods=['GET'])
@login_required
def checkout_success():
    session_id = request.args.get('session_id')
    if not session_id:
        flash("Invalid session.")
        return redirect(url_for('index'))

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            basket_items = db.session.scalars(sa.select(Basket).where(Basket.user_id == current_user.id)).all()
            for basket_item in basket_items:
                product = db.session.scalar(sa.select(Product).where(Product.id == basket_item.product_id))
                if product:
                    if product.stock >= basket_item.quantity:
                        product.stock -= basket_item.quantity
                    else:
                        flash(f"Insufficient stock for {product.title}. Could not fulfill the order.")
                        return redirect(url_for('basket'))


            db.session.execute(sa.delete(Basket).where(Basket.user_id == current_user.id))
            db.session.commit()

            flash("Thank you for your purchase! Your order has been successfully processed.")
            return render_template('checkout_success.html', title='Checkout Successful')
        else:
            flash("Payment not successful. Please try again.")
            return redirect(url_for('basket'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('basket'))


