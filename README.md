# Online Book Store

A complete, functional Online Book Store website developed using Flask, SQLAlchemy, and Bootstrap. This project features user authentication, book management (CRUD), searching, and a purchasing system.

## Features

*   **User Authentication**: Register, Login, Logout using `Flask-Login`.
*   **Admin Dashboard**: Add, Delete, and View all books (Secure file uploads).
*   **Browse & Search**: Homepage with book grid and search functionality.
*   **Book Details**: Detailed view of each book with stock status.
*   **Shopping System**: Buy books and view order history ("My Orders").
*   **Responsive Design**: Built with Bootstrap 5 and custom CSS.

## Tech Stack

*   **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
*   **Backend**: Python, Flask
*   **Database**: SQLite (via Flask-SQLAlchemy)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd online_book_store
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python3 app.py
    ```

5.  **Access the website:**
    Open your browser and navigate to `http://127.0.0.1:5000`.

## User Guide

### Admin Access
By default, newly registered users are standard users. To make a user an admin, you must manually update the `is_admin` flag in the database or use a database tool (e.g., DB Browser for SQLite) to edit `site.db`.

### How to Buy
1.  Register/Login to your account.
2.  Browse books on the home page or use the search bar.
3.  Click "View Details" on a book.
4.  Click "Buy Now" to purchase.
5.  Go to "My Orders" to see your purchase history.

## Project Structure
```text
online_book_store/
├── app.py                  # Entry point
├── config.py               # App configuration
├── requirements.txt        # Dependencies
└── website/
    ├── __init__.py         # App factory
    ├── models.py           # Database models
    ├── views.py            # Routes (Home, Admin, Orders)
    ├── auth.py             # Auth routes
    ├── templates/          # HTML Templates
    └── static/             # CSS, JS, Images

## API Documentation

### Get All Books
*   **URL**: `/api/books`
*   **Method**: `GET`
*   **Response**: JSON array of book objects.
*   **Example**:
    ```json
    {
      "books": [
        {
          "author": "F. Scott Fitzgerald",
          "id": 1,
          "image_url": "gatsby.jpg",
          "price": 12.99,
          "stock": 50,
          "title": "The Great Gatsby"
        }
      ]
    }
    ```
```
