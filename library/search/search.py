
from flask import Blueprint
from flask import render_template, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import library.utilities.utilities as utilities
import library.books.services as services


search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search_book', methods=['GET', 'POST'])
def search_book():
    form = searchForm()
    books = utilities.get_all_books()
    books_by_year = utilities.get_books_by_year()
    years = [book.release_year for book in books_by_year]
    publishers = utilities.get_publishers_by_name()
    authors = utilities.get_authors_by_name()

    books_by_authors_dict = services.get_authors_by_name_dict(books, authors)
    books_by_year_dict = services.get_books_by_year_dict(books_by_year)
    books_by_publisher_dict = services.get_books_by_publisher_dict(books, publishers)

    if form.validate_on_submit():
        items_found = []
        # searches by title
        for book in books:
            if form.keyword.data.lower() in book.title.lower():
                items_found.append(book)
        # searches by author
        for author in authors:
            if form.keyword.data.lower() in author.full_name.lower():
                for book in books_by_authors_dict[author.full_name]:
                    items_found.append(book)
        # searches by publisher
        for publisher in publishers:
            if form.keyword.data.lower() in publisher.name.lower():
                for book in books_by_publisher_dict[publisher.name]:
                    items_found.append(book)
        # searches by release year
        for year in years:
            if str(form.keyword.data) == str(year):
                for book in books_by_year_dict[int(year)]:
                    items_found.append(book)
        
        # return distinct list of found items:
        distinct_items = []
        for book in items_found:
            if book not in distinct_items:
                distinct_items.append(book)

        return render_template(
            'search/search.html',
            form = form, 
            handler_url = url_for('search_bp.search_book'),
            books = distinct_items,
            length = len(distinct_items),
            no_book_found_statement = True
        )

    else:
        return render_template(
            'search/search.html',
            search_type = "a book",
            form = form,
            handler_url = url_for('search_bp.search_book'),
            books = [],
            length = 0
        )


class searchForm(FlaskForm):
    keyword = StringField('Search for a book by title, author, publisher, or release year', [
        DataRequired(message='Keyword needed')])
    submit = SubmitField('go!')











