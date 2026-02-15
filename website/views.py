from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Book, Order, OrderItem, Review
from flask_mail import Message
from . import db, mail
import os
from functools import wraps

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'website/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Access denied. Admin rights required.", category='error')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

@views.route('/')
def home():
    query = request.args.get('q')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort')

    db_query = Book.query

    if query:
        db_query = db_query.filter(Book.title.contains(query) | Book.author.contains(query))
    
    if min_price is not None:
        db_query = db_query.filter(Book.price >= min_price)
    
    if max_price is not None:
        db_query = db_query.filter(Book.price <= max_price)
        
    if sort_by == 'price_asc':
        db_query = db_query.order_by(Book.price.asc())
    elif sort_by == 'price_desc':
        db_query = db_query.order_by(Book.price.desc())
        
    books = db_query.all()
    return render_template("home.html", user=current_user, books=books)

@views.route('/api/books')
def api_books():
    query = request.args.get('q')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort')

    db_query = Book.query

    if query:
        db_query = db_query.filter(Book.title.contains(query) | Book.author.contains(query))
    
    if min_price is not None:
        db_query = db_query.filter(Book.price >= min_price)
    
    if max_price is not None:
        db_query = db_query.filter(Book.price <= max_price)
        
    if sort_by == 'price_asc':
        db_query = db_query.order_by(Book.price.asc())
    elif sort_by == 'price_desc':
        db_query = db_query.order_by(Book.price.desc())

    books = db_query.all()
    data = []
    for book in books:
        data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'stock': book.stock,
            'image_url': book.image_url
        })
    return {'books': data}

@views.route('/book/<int:id>', methods=['GET', 'POST'])
def book_details(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You must be logged in to post a review.", category='error')
            return redirect(url_for('views.login'))

        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if not rating or not comment:
            flash("Rating and comment are required.", category='error')
        else:
            new_review = Review(user_id=current_user.id, book_id=book.id, rating=int(rating), comment=comment)
            db.session.add(new_review)
            db.session.commit()
            flash("Review added successfully!", category='success')
            return redirect(url_for('views.book_details', id=id))

    return render_template("book_details.html", user=current_user, book=book)

@views.route('/buy/<int:id>', methods=['POST'])
@login_required
def buy_book(id):
    # Instead of immediate buy, redirect to checkout
    return redirect(url_for('views.checkout', id=id))

@views.route('/checkout/<int:id>', methods=['GET', 'POST'])
@login_required
def checkout(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        if book.stock > 0:
            # Mock Payment Success
            # Create Order
            new_order = Order(user_id=current_user.id)
            db.session.add(new_order)
            db.session.commit()
            
            order_item = OrderItem(order_id=new_order.id, book_id=book.id, quantity=1, price_at_purchase=book.price)
            db.session.add(order_item)
            
            book.stock -= 1
            db.session.commit()
            
            # Send Email
            try:
                msg = Message(f"Order Confirmation - Order #{new_order.id}",
                              sender='noreply@onlinebookstore.com',
                              recipients=[current_user.email])
                msg.body = f"Thank you for your purchase of '{book.title}' for ${book.price}. Your order number is {new_order.id}."
                mail.send(msg)
                flash('Payment successful! Order confirmation email sent.', category='success')
            except Exception as e:
                print(f"Email error: {e}")
                flash('Payment successful! (Email could not be sent - Dev Mode)', category='success')
                
            return redirect(url_for('views.orders'))
        else:
            flash('Book out of stock.', category='error')
            return redirect(url_for('views.home'))

    return render_template("checkout.html", user=current_user, book=book)

@views.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).all()
    return render_template("orders.html", user=current_user, orders=orders)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    # Decorator handles permission check
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        
        # Image Upload
        file = request.files.get('image')
        
        if not title or not author or not price:
            flash('Please fill in all required fields.', category='error')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Ensure directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            new_book = Book(title=title, author=author, description=description, 
                            price=float(price), stock=int(stock), image_url=filename)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', category='success')
        else:
            flash('Invalid image type or no image uploaded.', category='error')

    books = Book.query.all()
    return render_template("admin/dashboard.html", user=current_user, books=books)

@views.route('/delete-book/<int:id>')
@login_required
@admin_required
def delete_book(id):
    # Decorator handles permission check
    
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', category='success')
    return redirect(url_for('views.admin'))
