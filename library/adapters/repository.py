import abc

from library.domain.model import Publisher, Author, Book, Review, BooksInventory, User 


repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    # GETTERS / SETTERS
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
    @abc.abstractmethod
    def get_user(self, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_author(self, author: Author):
        raise NotImplementedError
    @abc.abstractmethod
    def get_author(self):
        raise NotImplementedError
    @abc.abstractmethod
    def get_authors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_book(self, book: Book):
        raise NotImplementedError
    @abc.abstractmethod
    def get_book(self, id: int):
        raise NotImplementedError
    @abc.abstractmethod
    def get_all_books(self):
        raise NotImplementedError
    @abc.abstractmethod
    def get_number_of_books(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError
    @abc.abstractmethod
    def get_publisher(self, name):
        raise NotImplementedError
    @abc.abstractmethod
    def get_publishers(self):
        raise NotImplementedError
    
    # RETURN LISTS OF OBJECTS ORDERED BY ATTRIBUTE
    @abc.abstractmethod
    def get_books_for_author(self, author_name: str):
        raise NotImplementedError
    @abc.abstractmethod
    def order_books_by_title(self, books):
        raise NotImplementedError
    @abc.abstractmethod
    def order_books_by_year(self, books):
        raise NotImplementedError
    @abc.abstractmethod
    def order_authors(self, authors):
        raise NotImplementedError
    @abc.abstractmethod
    def order_publishers(self, publishers):
        raise NotImplementedError
    
    # METHODS FOR BROWSING
    @abc.abstractmethod
    def get_year_of_previous_book(self, books_by_year_dict, current_year):
        raise NotImplementedError
    @abc.abstractmethod
    def get_year_of_next_book(self, books_by_year_dict, current_year):
        raise NotImplementedError

    # REVIEWS
    @abc.abstractmethod
    def create_review(self, book: Book):
        raise NotImplementedError
    
    @abc.abstractmethod
    def load_csv_review(self, book_id, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, book_id, review: Review):
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        raise NotImplementedError








