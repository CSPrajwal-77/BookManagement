from website import create_app, db
from website.models import Book
import requests
import os

app = create_app()

def add_more_books():
    new_books = [
        {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "description": "The Fellowship of the Ring.",
            "price": 25.99,
            "stock": 15,
            "image_url": "lotr.jpg",
            "download_url": "https://covers.openlibrary.org/b/id/8386348-L.jpg"
        },
        {
            "title": "Harry Potter and the Sorcerer's Stone",
            "author": "J.K. Rowling",
            "description": "A young wizard's journey begins.",
            "price": 19.99,
            "stock": 50,
            "image_url": "harry.jpg",
             "download_url": "https://covers.openlibrary.org/b/id/10522853-L.jpg"
        },
         {
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "description": "A story about following your dreams.",
            "price": 14.50,
            "stock": 40,
            "image_url": "alchemist.jpg",
             "download_url": "https://covers.openlibrary.org/b/id/7288647-L.jpg"
        },
        {
            "title": "Rich Dad Poor Dad",
            "author": "Robert Kiyosaki",
            "description": "What the rich teach their kids about money.",
            "price": 16.99,
            "stock": 35,
            "image_url": "richdad.jpg",
             "download_url": "https://covers.openlibrary.org/b/id/12779770-L.jpg"
        }
    ]

    save_dir = "website/static/images"
    os.makedirs(save_dir, exist_ok=True)

    with app.app_context():
        for book_data in new_books:
            # Download Image
            try:
                print(f"Downloading cover for {book_data['title']}...")
                response = requests.get(book_data['download_url'], timeout=10)
                if response.status_code == 200:
                    with open(os.path.join(save_dir, book_data['image_url']), 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"Failed to download image for {book_data['title']}")
            except Exception as e:
                print(f"Error downloading image: {e}")

            # Add to DB
            if not Book.query.filter_by(title=book_data['title']).first():
                book = Book(
                    title=book_data['title'],
                    author=book_data['author'],
                    description=book_data['description'],
                    price=book_data['price'],
                    stock=book_data['stock'],
                    image_url=book_data['image_url']
                )
                db.session.add(book)
                print(f"Added book: {book_data['title']}")
            else:
                print(f"Book already exists: {book_data['title']}")
        
        db.session.commit()
        print("More books added successfully!")

if __name__ == "__main__":
    add_more_books()
