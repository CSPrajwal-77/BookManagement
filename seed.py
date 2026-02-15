from website import create_app, db
from website.models import Book, User
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        # Create Tables
        db.create_all()

        # Check if Admin exists
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                email='admin@example.com',
                first_name='Admin',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            print("Admin user created (email: admin@example.com, password: admin123)")

        # Sample Books
        books = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic novel of the Jazz Age.",
                "price": 12.99,
                "stock": 50,
                "image_url": "gatsby.jpg" 
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "description": "A dystopian social science fiction novel and cautionary tale.",
                "price": 9.99,
                "stock": 100,
                "image_url": "1984.jpg"
            },
               {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.",
                "price": 14.99,
                "stock": 30,
                "image_url": "mockingbird.jpg"
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "description": "A romantic novel of manners written by Jane Austen.",
                "price": 11.50,
                "stock": 40,
                "image_url": "pride.jpg"
            },
             {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A story about a few days in the life of a teenage rebel.",
                "price": 10.99,
                "stock": 60,
                "image_url": "catcher.jpg"
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "description": "A fantasy novel and children's book by English author J. R. R. Tolkien.",
                "price": 15.99,
                "stock": 25,
                "image_url": "hobbit.jpg"
            }
        ]

        for book_data in books:
            if not Book.query.filter_by(title=book_data['title']).first():
                book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    description=book_data['description'],
                    price=book_data['price'],
                    stock=book_data['stock'],
                    image_url="" # Placeholder, normally would be a filename
                )
                db.session.add(book)
                print(f"Book added: {book_data['title']}")
        
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
