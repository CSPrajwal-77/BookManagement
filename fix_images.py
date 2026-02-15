from website import create_app, db
from website.models import Book

app = create_app()

def fix_images():
    with app.app_context():
        books_update = {
            "The Great Gatsby": "gatsby.jpg",
            "1984": "1984.jpg",
            "To Kill a Mockingbird": "mockingbird.jpg",
            "Pride and Prejudice": "pride.jpg",
            "The Catcher in the Rye": "catcher.jpg",
            "The Hobbit": "hobbit.jpg"
        }

        for title, filename in books_update.items():
            book = Book.query.filter_by(title=title).first()
            if book:
                book.image_url = filename
                print(f"Updated {title} with {filename}")
        
        db.session.commit()
        print("Database images updated successfully!")

if __name__ == "__main__":
    fix_images()
