import csv
from pathlib import Path
from datetime import date, datetime, time

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository
from library.domain.model import User, Review, Book, Author, Publisher, make_review
from library.adapters.jsondatareader import BooksJSONReader


def load_books_and_authors(data_path: Path, repo: AbstractRepository, database_mode: bool):
    authors = str(data_path / 'book_authors_excerpt.json')
    books = str(data_path / 'comic_books_excerpt.json')
    reader = BooksJSONReader(books, authors)
    reader.read_json_files()
   
    if database_mode == True:
        list_of_authors = []
        list_of_publishers = []
        list_of_books = []
        list_of_reviews = []
        # Create new objects, based on JSON book objects
        for book in reader.dataset_of_books:
            # AUTHORS
            for author in book.authors:
                new_author = Author(
                    author.unique_id, 
                    author.full_name
                )
                if new_author not in list_of_authors:
                    list_of_authors.append(new_author)

            # PUBLISHERS
            if book.publisher not in list_of_publishers:
                list_of_publishers.append(book.publisher)

            # BOOKS
            new_book = Book(
                book.book_id, 
                book.title
            )
            new_book.description = book.description
            new_book.num_pages = book.num_pages
            if book.release_year is not None:
                new_book.release_year = book.release_year

            # Connect book with newly created Publisher objects
            for publisher in list_of_publishers:
                if book.publisher.name == publisher.name:
                    new_book.publisher = publisher

            # Connect book to newly created Authors objects
            for new_author in list_of_authors:
                for author in book.authors:
                    if author.unique_id == new_author.unique_id:
                        new_book.add_author(new_author)            
            
            list_of_books.append(new_book)

        
        # load reviews
        reviews_filename = str(Path(data_path) / "reviews.csv")
        for data_row in read_csv_file(reviews_filename):

            book_id = int(data_row[1])
            book = [book for book in list_of_books if book.book_id == book_id][0]

            user_name = data_row[0]
            user = repo.get_user(user_name)
            
            review = Review(
                book = book, 
                review_text = data_row[2], 
                rating = int(data_row[3]), 
                user = user, 
                timestamp = datetime.fromisoformat(data_row[4])
            )

            if review not in list_of_reviews:
                list_of_reviews.append(review)
        
        # Loading new objects into the repo
        for book in list_of_books:
            repo.add_book(book)

        for author in list_of_authors:
            repo.add_author(author)

        for publisher in list_of_publishers:
            repo.add_publisher(publisher)

        
        for review in list_of_reviews:
            try:
                repo.add_review(review)
            except:
                pass

    else:
        for book in reader.dataset_of_books:
            repo.add_book(book)
            for author in book.authors:
                if author not in repo.get_authors():
                    repo.add_author(author)
            if book.publisher.name != "N/A":
                repo.add_publisher(book.publisher)
            repo.create_review(book)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        for row in reader:
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path, repo: AbstractRepository):
    users = list()
    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User (
            user_name = data_row[1],
            password = generate_password_hash(data_row[2]) 
        )
        repo.add_user(user)
        

def load_reviews(data_path: Path, repo: AbstractRepository):
    """ MOVED TO load_books_and_authors for ACID principles.

    list_of_reviews = []
    reviews_filename = str(Path(data_path) / "reviews.csv")
    
    for data_row in read_csv_file(reviews_filename):

        book = repo.get_book(int(data_row[1]))

        user_name = data_row[0]
        user = repo.get_user(user_name)
        
        review = Review(
            book = book, 
            review_text = data_row[2], 
            rating = int(data_row[3]), 
            user = user, 
            timestamp = datetime.fromisoformat(data_row[4])
        )

        print(review)

        if review not in list_of_reviews:
            list_of_reviews.append(review)

    for review in list_of_reviews:
        repo.add_review(review)
        
    """
    pass

    
    
    
    
