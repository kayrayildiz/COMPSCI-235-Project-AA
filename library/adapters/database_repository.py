from typing import List
from flask import _app_ctx_stack
from sqlalchemy import desc, asc
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.sql.expression import asc, text

from library.adapters.repository import AbstractRepository
from library.domain.model import User, Book, Author, Publisher, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    # SESSION MANAGEMENT
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # REPOSITORY METHODS
        # USER
    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            pass

        return user

    def add_to_reading_list(self, user: User, book: Book):
        current_user_id = user.id
        current_book_id = book.book_id
        # Use native SQL to retrieve ids, since there is no mapped class for the user_reading_list table.
        sql_statement = text("""INSERT INTO user_reading_lists(user_id, book_id)  VALUES(:user_id, :book_id)""")
        self._session_cm.session.execute(sql_statement, {"user_id": current_user_id, "book_id": current_book_id})
        self._session_cm.session.commit()


        """ Cant do this because its not mapped to anything
        with self._session_cm as scm:
            scm.session.add(user, book)
            scm.commit() # needs work
        """

        # AUTHOR
    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_author(self, id: int):
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._Author__id == id).one()
        except NoResultFound:
            pass
        return author

    def get_authors(self):
        authors = self._session_cm.session.query(Author).order_by(asc(Author._Author__full_name)).all()

        return authors

        # BOOK
    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()

    def get_book(self, id: int):
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            pass
        return book
    
    def get_all_books(self) -> List[Book]:
        books = self._session_cm.session.query(Book).all()
        return books

    def get_number_of_books(self):
        number_of_books = self._session_cm.session.query(Book).count()
        return number_of_books

        # PUBLISHER
    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()
    
    def get_publisher(self, name):
        publisher = None
        try:
            publisher = self._session_cm.session.query(Publisher).filter(Publisher._Publisher__name == name).one()
        except NoResultFound:
            pass
        return publisher

    def get_publishers(self):
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

        # REVIEW
    def create_review(self, book: Book): # This is only necessary to fulfill Abstract Repo constraints.
        pass # "creation" of reviews into the database is done in the add_review method.

    def add_review(self, book_id, review: Review):
        #super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def load_csv_review(self, book_id, review: Review): # This is only necessary to fulfill Abstract Repo constraints.
        pass

    def get_reviews(self):
        # Reviews are accessed as a list of dictionaries: [{'book_id': 123, 'reviews': [<review1>, <review2>...]}]
        reviews = self._session_cm.session.query(Review).all() 
        
        reviews_dictionary_list = []
        for book in self.get_all_books():
            temp_dict = {'book_id': book.book_id, 'reviews': []}
            reviews_dictionary_list.append(temp_dict)

        for review in reviews:
            for book_dictionary in reviews_dictionary_list:
                if book_dictionary['book_id'] == review.book.book_id:
                    book_dictionary['reviews'].append(review)
        
        return reviews_dictionary_list
        
    
        # BROWSING METHODS
    def get_year_of_next_book(self, books_by_year_dict, current_year):
        keys = [key for key in books_by_year_dict.keys()]
        current_year_index = keys.index(current_year)
        prev_year_index = (current_year_index - 1) % len(keys)
        prev_year = keys[prev_year_index]
        return prev_year

    def get_year_of_previous_book(self, books_by_year_dict, current_year):
        keys = [key for key in books_by_year_dict.keys()]
        current_year_index = keys.index(current_year)
        next_year_index = (current_year_index + 1) % len(keys)
        next_year = keys[next_year_index]
        return next_year

        # RETURN LISTS OF OBJECTS ORDERED BY ATTRIBUTE
    def get_books_for_author(self, author_name: str): 
        """
            -> need to use many-to-many book/author relationship for the future?
            this method only returns a list of books for ONE auther, specified in the argument.
            for now method just loops through authors and books lists respectively to find correct
            books corresponding to specific author.
        """
        books_by_author_list = []

        authors = self._session_cm.session.query(Author).order_by(desc(Author._Author__full_name)).all()
        author = next((author for author in authors if author.full_name == author_name), None)
        
        books = self._session_cm.session.query(Book).order_by(desc(Book._Book__book_id)).all()
        for book in books:
            for an_author in book.authors:
                if an_author == author:
                    books_by_author_list.append(book)

        return books_by_author_list

    def order_books_by_title(self, books):
        books = self._session_cm.session.query(Book).order_by(asc(Book._Book__title)).all()
        return books

    def order_books_by_year(self, books):
        books = self._session_cm.session.query(Book).order_by(desc(Book._Book__release_year)).all()
        for i in range(len(books)-1, -1, -1):
            if books[i].release_year == None: # get rid of None - otherwise you cannot loop through release years as integers
                books.pop(i)
        return books

    def order_authors(self, authors):
        authors = self._session_cm.session.query(Author).order_by(asc(Author._Author__full_name)).all()
        return authors

    def order_publishers(self, publishers):
        publishers = self._session_cm.session.query(Publisher).order_by(asc(Publisher._Publisher__name)).all()
        return publishers