from library.adapters.repository import AbstractRepository

from library.domain.model import Review


class NonExistentBookException(Exception):
    pass


class UnknownUserException(Exception):
    pass


# GET CERTAIN OBJECT BY ATTRIBUTES
def get_years(current_year, repo: AbstractRepository):
    books = repo.get_all_books()
    books_by_year = repo.order_books_by_year(books)
    books_by_year_dict = get_books_by_year_dict(books_by_year)
    prev_year = repo.get_year_of_previous_book(books_by_year_dict, current_year)
    next_year = repo.get_year_of_next_book(books_by_year_dict, current_year)
    return prev_year, next_year


def get_author(author_id, repo: AbstractRepository):
    return repo.get_author(author_id)


def get_book(book_id, repo: AbstractRepository):
    return repo.get_book(book_id)


def get_books_by_author(author_name, repo: AbstractRepository):
    author_books = repo.get_books_for_author(author_name)
    return author_books


# DICTIONARIES
# DICTIONARY = {2016: [<Book>, <Book>...], 2013: [<Book>]} etc.
def get_books_by_year_dict(books_by_year):
    books_by_year_dict = {}
    for book in books_by_year:
        if book.release_year not in books_by_year_dict.keys() and book.release_year != None:
            books_by_year_dict[book.release_year] = [book]
        else:
            if book.release_year != None:
                books_by_year_dict[book.release_year].append(book)
    return books_by_year_dict


# DICTIONARY = {'author_name': [<book1>, <book2>], ...}
def get_authors_by_name_dict(books, authors_by_name):
    books_by_authors = {}
    for author in authors_by_name:
        for book in books:
            if author in book.authors:
                if author.full_name not in books_by_authors.keys():
                    books_by_authors[author.full_name] = [book]
                else:
                    books_by_authors[author.full_name].append(book)
    return books_by_authors


# DICTIONARY = {'publisher_name': [<book1>, <book2>], ...}
def get_books_by_publisher_dict(books, publishers_by_name):
    books_by_publishers = {}
    for publisher in publishers_by_name:
        for book in books:
            if publisher == book.publisher:
                if publisher.name not in books_by_publishers.keys():
                    books_by_publishers[publisher.name] = [book]
                else:
                    if book not in books_by_publishers[publisher.name]:
                        books_by_publishers[publisher.name].append(book)
    return books_by_publishers


# AUTHENTICATION
# ______________________________________________________________________

def add_review(book_id: int, review_text: str, rating: int, user_name: str,
               repo: AbstractRepository):  # can have user: User if we want to add reviews to a specific User's data
    book = repo.get_book(book_id)
    if book is None:
        raise NonExistentBookException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    review = Review(book, review_text, rating, user)
    book.add_review(review)
    # user.add_review(review) <- later
    repo.add_review(book_id, review)


def add_to_readinglist(user_name: str, book_id: int, repo: AbstractRepository):
    user = repo.get_user(user_name)
    book = repo.get_book(book_id)
    
    repo.add_to_reading_list(user, book)
    user.read_a_book(book)
