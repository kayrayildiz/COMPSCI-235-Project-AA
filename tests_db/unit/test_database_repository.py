from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.authentication import services
from library.domain.model import Publisher, Author, Book, Review, User
from library.adapters.repository import RepositoryException

from library.books.services import get_books_by_publisher_dict, get_books_by_year_dict, get_authors_by_name_dict
from library.utilities.services import get_all_books, get_publishers_by_name, get_books_by_year, get_authors_by_name, get_recommended_books

# everything failing because UNIQUE constraint failed: authors.author_id
def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('test_user', '123456789')
    repo.add_user(user)
    repo.add_user(User('test_user2', '123456789'))
    user2 = repo.get_user('test_user')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('fmercury')

    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('prince')

    assert user is None

def test_repository_can_retrieve_book_count(session_factory):                               
    repo = SqlAlchemyRepository(session_factory)
    number_of_books = repo.get_number_of_books()

    assert number_of_books == 20

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_books = repo.get_number_of_books()
    test_book = Book(123, 'test_book')
    repo.add_book(test_book)

    assert repo.get_book(123) == test_book

def test_repository_can_retrieve_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    book = repo.get_book(13340336)

    # Check that the Book has the expected title.
    assert book.title == '20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)'

    # Check that the Book is reviewed as expected.
    
   
def test_repository_does_not_retrieve_a_non_existent_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    article = repo.get_book(321)

    assert article is None

def test_repository_can_order_books_by_year(session_factory): 
    repo = SqlAlchemyRepository(session_factory)
    all_books = repo.get_all_books()
    books = repo.order_books_by_year(all_books)
    specific_year = 2016
    items_found = books[0:5]
    book_titles = [book.title for book in items_found]
    
    # check the first 5 books are correct
    assert book_titles == ['War Stories, Volume 3', 'Crossed, Volume 15', 'Crossed + One Hundred, Volume 2 (Crossed +100 #2)', 'War Stories, Volume 4', 'Cruelle']
    
    # check the first 5 books are all from specific_year
    for book in items_found:
        assert int(book.release_year) == specific_year

def test_search_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    search_field = 2016
    items_should_be_found = 5
    items_found = []

    books_by_year = get_books_by_year(repo)
    books_by_year_dict = get_books_by_year_dict(books_by_year)

    items_found = books_by_year_dict[search_field]

    for book in items_found:
        assert book.release_year == 2016

    assert len(items_found) == items_should_be_found 

def test_repository_returns_correct_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    books_by_year = get_books_by_year(repo)
    books_by_year_dict = get_books_by_year_dict(books_by_year)

    previous_year = repo.get_year_of_previous_book(books_by_year_dict, 2016)
    next_year = repo.get_year_of_next_book(books_by_year_dict, 2016)

    assert next_year == 1997
    assert previous_year == 2014

def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_author = Author(123, "test_author")
    repo.add_author(test_author)

    assert test_author in repo.get_authors()

def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    test_book = repo.get_book(13340336)
    user = User('test_user', '123456789')
    test_review = Review(test_book, "I hate covid lockdown! :)", 5, user)
    repo.add_review(13340336, test_review)

    for book_dictionary in repo.get_reviews():
        if book_dictionary['book_id'] == 13340336:
            assert test_review in book_dictionary['reviews']

def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 20

