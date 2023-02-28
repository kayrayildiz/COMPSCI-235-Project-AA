import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import User, Book, Author, Review, Publisher


def insert_user(empty_session, values=None):
    new_name = "new_test_user"
    new_password = "Password1"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)', {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name', {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)', {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (book_id, title, description, publisher_id, release_year, num_pages) VALUES '
        '(123, "test_title", "This is a test book description.", 1, 2000, 100)'
    )
    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def insert_author(empty_session):
    empty_session.execute('INSERT INTO authors (author_name) VALUES ("test_author_name1"), ("test_author_name2")')
    rows = list(empty_session.execute('SELECT id from authors'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book_author_associations(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO book_authors (book_id, author_id) VALUES (:book_id, :author_id)'
    for author_key in author_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'author_id': author_key})

def insert_reviewed_books(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, user_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :book_id, 1, "Review description 1", 4, :timestamp_1),'
        '(:user_id, :book_id, 1, "Review description 2", 5, :timestamp_2)',
        {'user_id': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def make_book():
    book = Book(123, "My Test Book Title")
    return book

def make_user():
    user = User("test_user1", "Password1")
    return user

def make_author():
    author = Author(123456, "Test Author Name")
    return author

def test_loading_of_users(empty_session):
    users = list()
    users.append(("test_user1", "Password1"))
    users.append(("test_user2", "Password1"))
    insert_users(empty_session, users)

    expected = [
        User("test_user1", "Password1"),
        User("test_user2", "Password1")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("test_user1", "Password1")]

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("test_user1", "Password1"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("test_user1", "Password1")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id

def test_loading_of_reviewed_book(empty_session): # F: REVIEWS CURRENTLY UNDER CONSTRUCTION IN ORM
    insert_reviewed_books(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book

def test_saving_of_review(empty_session): # F: REVIEWS CURRENTLY UNDER CONSTRUCTION IN ORM
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("test_user1", "Password1"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "test_user1").one()

    review_text = "Some review text."
    review = Review(book, review_text, 5, user)
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, book_id FROM reviews'))

    assert rows == [(user_key, book_key)]

def test_saving_of_book(empty_session):
    book = make_book() # Book(123, "My Test Book Title")
    empty_session.add(book)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT book_id, title FROM books'))
    assert rows == [(123, "My Test Book Title")]
