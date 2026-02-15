from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True) # URL or path to image
    stock = db.Column(db.Integer, default=0)
    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5
    comment = db.Column(db.Text, nullable=True)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_ordered = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(50), default='Pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # We can store the price at time of purchase to avoid issues if book price changes
    price_at_purchase = db.Column(db.Float, nullable=False)

    book = db.relationship('Book')

    @property
    def total_price(self):
        return self.price_at_purchase * self.quantity
