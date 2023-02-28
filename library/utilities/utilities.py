from flask import Blueprint, url_for

import library.adapters.repository as repo
import library.utilities.services as services


utilities_blueprint = Blueprint('utilities_bp', __name__)

# URL GENERATORS
def get_books_and_urls():
    books = services.get_books_by_title(repo.repo_instance)
    book_titles = [book.title for book in books]
    book_urls = dict()
    for book_title in book_titles:
        book_urls[book_title] = url_for('books_bp.browse_all', title=book_title)
    return book_urls

def get_readinglist_urls(reading_list):
    books_and_urls = {}
    for book in reading_list:
        books_and_urls[book.title] = url_for('books_bp.browse_all', title=book.title)
    return books_and_urls
    
def get_years_and_urls():
    release_years = services.get_books_by_year(repo.repo_instance)
    years = [book.release_year for book in release_years]
    year_urls = dict()
    for year in years:
        year_urls[year] = url_for('books_bp.books_by_year', year=year)
    return year_urls


def get_authors_and_urls():
    author_names = services.get_author_names(repo.repo_instance)
    author_urls = dict()
    for author_name in author_names:
        author_urls[author_name] = url_for('books_bp.books_by_author', author=author_name)
    return author_urls


def get_publishers_and_urls():
    publishers = services.get_publishers_by_name(repo.repo_instance)
    publisher_names = [publisher.name for publisher in publishers]
    publisher_urls = dict()
    for publisher_name in publisher_names:
        publisher_urls[publisher_name] = url_for('books_bp.books_by_publisher', publisher=publisher_name)
    return publisher_urls


# ORDERED BOOK GENERATORS
def get_all_books():
    books = services.get_all_books(repo.repo_instance)
    return books

   
def get_books_by_title():
    books_by_title = services.get_books_by_title(repo.repo_instance)
    return books_by_title


def get_books_by_year():
    books_by_year = services.get_books_by_year(repo.repo_instance)
    return books_by_year


def get_authors_by_name():
    authors_by_name = services.get_authors_by_name(repo.repo_instance)
    return authors_by_name


def get_publishers_by_name():
    publishers_by_name = services.get_publishers_by_name(repo.repo_instance)
    return publishers_by_name


# REVIEWS
def get_reviews():
    book_reviews_dict = services.get_reviews(repo.repo_instance)
    return book_reviews_dict

