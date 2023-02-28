from sqlalchemy import select, inspect

from library.adapters.orm import metadata

# all failing because UNIQUE constraint failed: authors.author_id
def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)

    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'publishers', 'reviews', 'user_reading_lists', 'users']

def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_id'])

        assert all_users == [3, 3]

def test_database_populate_select_all_reviews(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['reviews']])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['book_id'], row['review_text']))

        assert all_comments[0] == (1, 3, 13340336, 'This is a great book!')
        assert all_comments[1] == (2, 3, 13340336, 'This book was OK')

def test_database_populate_select_all_books(database_engine):
    with database_engine.connect() as connection:
        select_statement = select([metadata.tables['books']])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['book_id'], row['title']))

        nr_books = len(all_books)
        assert nr_books == 20

        assert all_books[0] == (707611, 'Superman Archives, Vol. 2')


