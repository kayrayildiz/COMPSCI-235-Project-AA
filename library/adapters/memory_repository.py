import csv
import operator
from pathlib import Path
from datetime import datetime
from bisect import insort_left
from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__users = list()
        self.__books = []
        self.__books_index = dict()
        self.__authors = list()
        self.__publishers = list()
        self.__reviews = list()

    # GETTERS AND SETTERS
    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name):
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_author(self, author_id):
        for author in self.__authors:
            if author.unique_id == author_id:
                return author

    def get_authors(self):
        return self.__authors

    def add_book(self, book: Book):
        insort_left(self.__books, book)
        self.__books_index[book.book_id] = book

    def get_book(self, id: int):
        for book in self.__books:
            if book.book_id == id:
                return book
        return None

    def get_all_books(self):
        return self.__books

    def get_number_of_books(self):
        return len(self.__books)

    def add_publisher(self, publisher: Publisher):
        self.__publishers.append(publisher)

    def get_publisher(self, name):
        for publisher in self.__publishers:
            if publisher.name == name:
                return publisher

    def get_publishers(self):
        return self.__publishers

    # RETURN LISTS OF OBJECTS ORDERED BY ATTRIBUTE
    def get_books_for_author(self, author_name: str):
        author = next((author for author in self.__authors if author.full_name == author_name), None)
        author_books = []
        for book in self.__books:
            for an_author in book.authors:
                if author == an_author:
                    author_books.append(book)
        return author_books

    def order_books_by_title(self, books): # SORTS BOOKS BY TITLE IN ALPHABETICAL ORDER
        books_by_title_list = sorted(books, key=operator.attrgetter("title"))
        return books_by_title_list

    def order_books_by_year(self, books): # ORDERS BOOKS BY RELEASE YEAR IN DESCENDING ORDER (NEWEST TO OLDEST)
        """ Some books dont have a release year - so we don't include them in this list """
        with_release_year = []
        without_release_year = []
        for book in books:
            if book.release_year is not None:
                with_release_year.append(book)
            else:
                without_release_year.append(book)
        books_by_year_list = sorted(with_release_year, key=operator.attrgetter("release_year"), reverse=True)
        return books_by_year_list

    def order_authors(self, authors): # SORTS AUTHORS IN ALPHABETICAL ORDER
        authors_ordered = sorted(authors, key=lambda x: x.full_name)
        return authors_ordered

    def order_publishers(self, publishers):
        publishers_ordered = sorted(publishers, key=lambda x: x.name)
        return publishers_ordered

    # METHODS FOR BROWSING BOOKS
    def get_year_of_previous_book(self, books_by_year_dict, current_year):
        keys = [key for key in books_by_year_dict.keys()]
        current_year_index = keys.index(current_year)
        prev_year_index = (current_year_index - 1) % len(keys)
        prev_year = keys[prev_year_index]
        return prev_year

    def get_year_of_next_book(self, books_by_year_dict, current_year):
        keys = [key for key in books_by_year_dict.keys()]
        current_year_index = keys.index(current_year)
        next_year_index = (current_year_index + 1) % len(keys)
        next_year = keys[next_year_index]
        return next_year

    # METHODS FOR REVIEWS
    def create_review(self, book: Book):
        self.__reviews.append({'book_id': book.book_id, 'reviews': []}) # stores book_id under 'book_id' and a list of respective reviews for the book under 'reviews'

    def load_csv_review(self, book_id, review: Review):
        for dictionary in self.__reviews:
            if dictionary['book_id'] == book_id:
                dictionary['reviews'].append(review)

    def add_review(self, book_id, review: Review):
        for dictionary in self.__reviews:
            if dictionary['book_id'] == book_id:
                dictionary['reviews'].append(review)
        
    def get_reviews(self):
        return self.__reviews

"""
def load_books_and_authors(data_path: Path, repo: MemoryRepository):
    authors = str(data_path / 'book_authors_excerpt.json')
    books = str(data_path / 'comic_books_excerpt.json')
    reader = BooksJSONReader(books, authors)
    reader.read_json_files()
    for book in reader.dataset_of_books:
        repo.add_book(book)
        for author in book.authors:
            if author not in repo.get_authors():
                repo.add_author(author)
        if book.publisher.name != "N/A":
            repo.add_publisher(book.publisher)
        repo.create_review(book)
"""



# LOADING CSV DATABASES
""" (commenting out for now)
def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        for row in reader:
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path, repo: MemoryRepository):
    users = list()
    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User (
            user_name = data_row[1],
            password = generate_password_hash(data_row[2]) 
        )
        repo.add_user(user)


def load_reviews(data_path: Path, repo: MemoryRepository):
    comments_filename = str(Path(data_path) / "reviews.csv")
    for data_row in read_csv_file(comments_filename):
        book = repo.get_book(int(data_row[1]))
        review = Review(
            book = book,
            review_text = data_row[2], 
            rating = int(data_row[3]), 
            user_name = data_row[0], 
            timestamp = datetime.fromisoformat(data_row[4]) 
        )
        repo.load_csv_review(book.book_id, review)
        book.add_review(review)
"""

# POPULATE
"""
def populate(data_path: Path, repo: MemoryRepository):
    # Load books and authors into the repository.
    load_books_and_authors(data_path, repo)

    # Load book reviews
    load_reviews(data_path, repo)

    # Load users to repo
    load_users(data_path, repo)
"""



