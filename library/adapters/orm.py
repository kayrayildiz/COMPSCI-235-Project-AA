from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import backref, mapper, relationship, synonym

from library.domain import model

metadata = MetaData()

# TABLE GENERATION
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255))
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=True),
    Column('publisher_id', ForeignKey('publishers.id'), nullable=True),
    Column('release_year', Integer),
    Column('num_pages', Integer)
)

authors_table = Table(
    'authors', metadata,
    Column('author_id', Integer, primary_key=True),
    Column('full_name', String(255)),
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
    Column('review_text', String(255)),
    Column('rating', Integer),
    Column('timestamp', DateTime, nullable=False)
)

# RELATIONSHIP TABLES
book_authors = Table( # ONE book, MANY authors
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('author_id', ForeignKey('authors.author_id'))
)

user_reading_lists = Table( # ONE user, MANY books
    'user_reading_lists', metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id'))
)


# MAPPER
def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password, 
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
        '_User__read_books': relationship(model.Book, secondary=user_reading_lists),
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__publisher': relationship(model.Publisher), 
        '_Book__release_year': books_table.c.release_year,
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
        '_Book__authors': relationship(model.Author, secondary=book_authors),
        '_Book__num_pages': books_table.c.num_pages
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.author_id, 
        '_Author__full_name': authors_table.c.full_name,
    })
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__id': publishers_table.c.id,
        '_Publisher__name': publishers_table.c.name
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    