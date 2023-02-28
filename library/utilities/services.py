from typing import Iterable


from library.adapters.repository import AbstractRepository
from library.domain.model import Book

from flask import url_for


# USEFUL METHODS
def get_all_books(repo: AbstractRepository):
    return repo.get_all_books()


def get_author_names(repo: AbstractRepository):
    authors = repo.get_authors()
    author_names = [author.full_name for author in authors]
    return author_names


# SPECIAL FEATURES
def get_readinglist_for_user(user_name, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user.read_books is not None:
        return user.read_books
    else:
        return []


def remove_from_reading_list(user_name, book: Book, repo: AbstractRepository):
    user = repo.get_user(user_name)
    user.remove_a_book(book)


def get_recommended_books(reading_list, repo: AbstractRepository):
    authors = []
    author_book_dict = {}
    for book in reading_list:
        for author in book.authors:
            if author not in authors:
                authors.append(author)
    
    for author in authors:
        author_book_dict[author.full_name] = repo.get_books_for_author(author.full_name)

    # DICTIONARY = {author_name: [{<book>: "url"}, {<book>: "url"}], author_name: [{<book>: "url"}]}
    for key, value in author_book_dict.items():
        for book in reading_list:
            if book in value:
                value.pop(value.index(book))
        value_list = []
        for book in value:
            url = url_for('books_bp.browse_all', title=book.title)
            value_list.append({'book': book, 'url': url})
        author_book_dict[key] = value_list
    return author_book_dict
    
# ORDER OBJECTS BY SPECIFIC ATTRIBUTES
def get_books_by_title(repo: AbstractRepository):
    books = repo.get_all_books()
    return repo.order_books_by_title(books)


def get_books_by_year(repo: AbstractRepository):
    books = repo.get_all_books()
    return repo.order_books_by_year(books)


def get_authors_by_name(repo: AbstractRepository):
    authors = repo.get_authors()
    return repo.order_authors(authors)


def get_publishers_by_name(repo: AbstractRepository):
    publishers = repo.get_publishers()
    return repo.order_publishers(publishers)


# REVIEWS
def get_reviews(repo: AbstractRepository):
    return repo.get_reviews()


# DICTIONARIES
def books_to_dict(book: Book):
    book_dict = {'year': book.release_year, 'title': book.title} # no image hyperlink yet

def books_to_dict(books: Iterable[Book]):
    return [books_to_dict(book) for book in books]

