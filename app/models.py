import random
import requests
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Product(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=False)
    price: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=True)
    image: so.Mapped[str] = so.mapped_column(sa.String(512), nullable=True)
    rating_rate: so.Mapped[float] = so.mapped_column(sa.Float, nullable=True)
    rating_count: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    stock: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Product {self.title} (${self.price})>"


class Basket(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    product_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    quantity: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)


def set_fake_stock():
    products = db.session.scalars(sa.select(Product)).all()
    for product in products:
        if product.stock is 0:
            product.stock = random.randint(1, 100)
    db.session.commit()


def populate_products():
    api_url = "https://fakestoreapi.com/products"
    response = requests.get(api_url)
    response.raise_for_status()
    products = response.json()

    for product in products:
        db_product = Product(
            id=product["id"],
            title=product["title"],
            price=product["price"],
            description=product["description"],
            category=product["category"],
            image=product["image"],
            rating_rate=product["rating"]["rate"],
            rating_count=product["rating"]["count"]
        )
        db.session.merge(db_product)

    db.session.commit()
    print("Database populated with products successfully.")
