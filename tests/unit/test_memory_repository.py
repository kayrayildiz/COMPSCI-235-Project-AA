import pytest
from library.books.services import get_books_by_publisher_dict, get_books_by_year_dict, get_authors_by_name_dict
from library.domain.model import Review, Author, User, Book
from library.utilities.services import get_all_books, get_publishers_by_name, get_books_by_year, get_authors_by_name, get_recommended_books


class TestMemoryRepository:
    def test_reviews(self, in_memory_repo):
        book = Book(30128855, "Cruelle")
        test_user = User('kayra', 123)
        review = Review(book, "review haha", 3, test_user)
        in_memory_repo.add_review(30128855, review)
        book_id = 30128855
        for item in in_memory_repo.get_reviews():
            if book_id in item.keys():
                assert review in item[book_id]

    def test_reading_list(self, in_memory_repo):
        user = User("haydengray", "")
        in_memory_repo.add_user(user)
        book = Book(30128855, "Cruelle")
        user.read_a_book(book)
        assert book in user.read_books

    def test_recommendations(self, in_memory_repo):
        user = User("haydengray", "")
        book = Book(30128855, "Cruelle")
        in_memory_repo.add_user(user)
        user.read_a_book(book)
        reading_list = user.read_books
        authors = []
        author_book_dict = {}
        for book in reading_list:
            for author in book.authors:
                if author not in authors:
                    authors.append(author)

        for author in authors:
            author_book_dict[author.full_name] = in_memory_repo.get_books_for_author(author.full_name)
        assert author_book_dict == get_recommended_books(user.read_books, in_memory_repo)

    def test_search_title(self, in_memory_repo):
        search_field = "The Switchblade Mamma"
        books = get_all_books(in_memory_repo)
        items_found = set()
        items_should_be_found = 1
        for book in books:
            if search_field.lower() in book.title.lower():
                items_found.add(book)
        all_titles_match = True
        for item in items_found:
            if search_field.lower() not in item.title.lower():
                all_titles_match = False
        assert len(items_found) == items_should_be_found and all_titles_match

    def test_search_author(self, in_memory_repo):
        search_field = "Naoki Urasawa"
        items_found = set()
        items_should_be_found = 3
        books = get_all_books(in_memory_repo)
        authors = get_authors_by_name(in_memory_repo)
        books_by_authors_dict = get_authors_by_name_dict(books, authors)
        for author in authors:
            if search_field.lower() in author.full_name.lower():
                for book in books_by_authors_dict[author.full_name]:
                    items_found.add(book)
        assert len(items_found) == items_should_be_found

    def test_search_publisher(self, in_memory_repo):
        search_field = "Avatar Press"
        items_should_be_found = 4
        items_found = set()
        books = get_all_books(in_memory_repo)
        publishers = get_publishers_by_name(in_memory_repo)
        books_by_publisher_dict = get_books_by_publisher_dict(books, publishers)
        for publisher in publishers:
            if search_field.lower() in publisher.name.lower():
                for book in books_by_publisher_dict[publisher.name]:
                    items_found.add(book)
        all_pubs_match = True
        for item in items_found:
            if item.publisher.name != "Avatar Press":
                all_pubs_match = False
        assert len(items_found) == items_should_be_found and all_pubs_match

    def test_search_release_year(self, in_memory_repo):
        search_field = 2016
        items_should_be_found = 5
        items_found = set()
        books_by_year = get_books_by_year(in_memory_repo)
        years = [book.release_year for book in books_by_year]
        books_by_year_dict = get_books_by_year_dict(books_by_year)
        for year in years:
            if str(search_field) == str(year):
                for book in books_by_year_dict[int(year)]:
                    items_found.add(book)
        all_years_match = True
        for item in items_found:
            if item.release_year != 2016:
                all_years_match = False
        assert len(items_found) == items_should_be_found and all_years_match

    def test_add_book(self, in_memory_repo):
        book = Book(30128855, "Cruelle")
        in_memory_repo.add_book(book)
        assert book in in_memory_repo.get_all_books()

    def test_get_book(self, in_memory_repo):
        book = Book(30128855, "Cruelle")
        in_memory_repo.add_book(book)
        assert book == in_memory_repo.get_book(30128855)

    def test_add_author(self, in_memory_repo):
        author = Author(1, "Hayden Gray")
        in_memory_repo.add_author(author)
        assert author in in_memory_repo.get_authors()

    def test_user(self, in_memory_repo):
        user = User("haydengray", "")
        in_memory_repo.add_user(user)
        assert user == in_memory_repo.get_user("haydengray")






