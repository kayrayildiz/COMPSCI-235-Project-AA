from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.books.services as services
from library.authentication.authentication import login_required



books_blueprint = Blueprint('books_bp', __name__)

    # BROWSE BY TITLE
@books_blueprint.route('/browse_all', methods=['GET'])
def browse_all():
    books = utilities.get_books_by_title()
    current_book = request.args.get('title')
    added = request.args.get('added')
    book_to_show_reviews = request.args.get('view_reviews') 
    book_titles = [book.title for book in books]
    
    book_reviews_dictionary = utilities.get_reviews() 
    books_by_title_dict = {}
    for book in books:
        number_of_reviews = 0
        for review in book.reviews:
            number_of_reviews += 1
        books_by_title_dict[book.title] = {'book': book, 'number_of_reviews': number_of_reviews}
    
    first_book = books[0].title
    last_book = books[-1].title
    
    if added is None:
        added = False
    else:
        added = True
    if current_book is None:
        current_book = first_book
    if book_to_show_reviews is None:
        book_to_show_reviews = books_by_title_dict[current_book]['book'].book_id
    else:
        book_to_show_reviews = int(book_to_show_reviews)
    
    
    current_book_index = book_titles.index(current_book)
    prev_book = book_titles[(current_book_index - 1) % len(books)]
    next_book = book_titles[(current_book_index + 1) % len(books)]

    prev_book_url = url_for('books_bp.browse_all', title=prev_book)
    first_book_url = url_for('books_bp.browse_all', title=first_book)
    next_book_url = url_for('books_bp.browse_all', title=next_book)
    last_book_url = url_for('books_bp.browse_all', title=last_book)

    # DICTIONARY = [{},{},{}]
    #            = [{'book_id': 123, 'reviews': [<Review>, <Review> ...]}, {'book_id': 234, 'reviews': [<Review> ...]}, ...]
    # adds 'view_reviews' and 'add_reviews' URLS to each dictionary - {'book_id': 123, 'reviews': [<review>], 'view_reviews': "url", 'add_review': "url"}
    for book_review in book_reviews_dictionary:
        book_review['view_reviews'] = url_for('books_bp.browse_all', title=current_book, view_reviews=book_to_show_reviews) # <- issue
        book_review['add_review'] = url_for('books_bp.review_book', book_id=book_to_show_reviews)  
    
    return render_template(
        'books/browse.html', 
        title = 'Browse all books', 
        specific_title = current_book, 
        current_books = [books_by_title_dict[current_book]['book']], 
        first_url = first_book_url, 
        last_url = last_book_url, 
        next_url = next_book_url,
        prev_url = prev_book_url,

        include_side_bar = True,
        select_type = 'a book', 
        select_urls = utilities.get_books_and_urls(), 

        write_review_url = url_for('books_bp.review_book', book_id=book_to_show_reviews), 
        number_of_reviews = books_by_title_dict[current_book]['number_of_reviews'], 
        all_books_page = True, 
        add_to_readinglist_url = url_for('books_bp.read_book', book_id=book_to_show_reviews), 
        added = added
    )




    # BROWSE BY YEAR
@books_blueprint.route('/books_by_year', methods=['GET'])
def books_by_year():
    books_by_year_list = utilities.get_books_by_year()
    books_by_year_dict = services.get_books_by_year_dict(books_by_year_list)

    year_keys = [key for key in books_by_year_dict.keys()]

    target_year = request.args.get('year')
    first_book = books_by_year_list[0].release_year
    last_book = year_keys[len(year_keys) - 1]

    if target_year is None:
        target_year = first_book
    else:
        target_year = int(target_year)
    
    prev_year, next_year = services.get_years(target_year, repo.repo_instance)
    if len(books_by_year_list) > 0:
        prev_book_url = url_for('books_bp.books_by_year', year=prev_year)
        first_book_url = url_for('books_bp.books_by_year', year=first_book)
        next_book_url = url_for('books_bp.books_by_year', year=next_year)
        last_book_url = url_for('books_bp.books_by_year', year=last_book)

        return render_template(
            'books/browse.html', 
            title = 'Books by release year', 
            specific_title = target_year, 
            current_books = books_by_year_dict[target_year],
            first_url = first_book_url, 
            last_url = last_book_url, 
            next_url = prev_book_url,
            prev_url = next_book_url, 

            include_side_bar = True,
            select_type = 'a release year', 
            select_urls = utilities.get_years_and_urls(), 
            all_books_page = False 
        )
    return redirect(url_for('home_bp.test'))


    # BROWSE BY AUTHOR
@books_blueprint.route('/books_by_author', methods=['GET'])
def books_by_author():
    books = utilities.get_all_books()
    authors_by_name = utilities.get_authors_by_name()
    authors_by_name_dict = services.get_authors_by_name_dict(books, authors_by_name)
    author_keys = [key for key in authors_by_name_dict.keys()]

    current_author = request.args.get('author')
    first_author = authors_by_name[0].full_name
    last_author = author_keys[len(author_keys) - 1]

    if current_author is None:
        current_author = first_author
    
    current_author_index = author_keys.index(current_author)

    prev_author = author_keys[(current_author_index - 1) % len(author_keys)]
    next_author = author_keys[(current_author_index + 1) % len(author_keys)]
    
    prev_author_url = url_for('books_bp.books_by_author', author=prev_author)
    first_author_url = url_for('books_bp.books_by_author', author=first_author)
    next_author_url = url_for('books_bp.books_by_author', author=next_author)
    last_author_url = url_for('books_bp.books_by_author', author=last_author)

    return render_template(
        'books/browse.html', 
        title = 'Books by author', 
        specific_title = current_author, 
        current_books = authors_by_name_dict[current_author], 
        first_url = first_author_url, 
        last_url = last_author_url,
        next_url = next_author_url, 
        prev_url = prev_author_url,

        include_side_bar = True,
        select_type = 'an author', 
        select_urls = utilities.get_authors_and_urls(), 
        all_books_page = False 
    )


    # BROWSE BY PUBLISHER
@books_blueprint.route('/books_by_publisher', methods=['GET'])
def books_by_publisher():
    books = utilities.get_all_books()
    publishers_by_name = utilities.get_publishers_by_name()
    books_by_publisher_dict = services.get_books_by_publisher_dict(books, publishers_by_name)
    publisher_keys = [key for key in books_by_publisher_dict.keys()]

    current_publisher = request.args.get('publisher')
    first_publisher = publishers_by_name[0].name
    last_publisher = publisher_keys[len(publisher_keys) - 1]

    if current_publisher is None:
        current_publisher = first_publisher
    
    current_publisher_index = publisher_keys.index(current_publisher)

    prev_publisher = publisher_keys[(current_publisher_index - 1) % len(publisher_keys)]
    next_publisher = publisher_keys[(current_publisher_index + 1) % len(publisher_keys)]
    
    prev_publisher_url = url_for('books_bp.books_by_publisher', publisher=prev_publisher)
    first_publisher_url = url_for('books_bp.books_by_publisher', publisher=first_publisher)
    next_publisher_url = url_for('books_bp.books_by_publisher', publisher=next_publisher)
    last_publisher_url = url_for('books_bp.books_by_publisher', publisher=last_publisher)

    return render_template(
        'books/browse.html', 
        title = 'Books by publisher', 
        specific_title = current_publisher, 
        current_books = books_by_publisher_dict[current_publisher], 
        first_url = first_publisher_url, 
        last_url = last_publisher_url,
        next_url = next_publisher_url, 
        prev_url = prev_publisher_url, 

        include_side_bar = True,
        select_type = 'a publisher', 
        select_urls = utilities.get_publishers_and_urls(), 
        all_books_page = False
    )

# AUTHENTICATION REQUIRED REVIEWS
# ______________________________________________________________________

    # REVIEWS
@books_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_book():
    user_name = session['user_name'] # gets user name of user currently in session
    form = reviewForm()
    if form.validate_on_submit():
        book_id = int(form.book_id.data)
        rating = int(form.rating.data)
        book = services.get_book(book_id, repo.repo_instance)
        services.add_review(book_id, form.review.data, rating, user_name, repo.repo_instance) 
        return redirect(url_for('books_bp.browse_all', title=book.title, view_reviews=book_id))
        
    if request.method == 'GET':
        book_id = int(request.args.get('book_id'))
        form.book_id.data = book_id
        
    else:
        book_id = int(form.book_id.data)
    
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        'books/reviews_on_books.html',
        title='Leave a review',
        book=book,
        form=form,
        handler_url=url_for('books_bp.review_book'),
    )

    # ADDING TO READING LIST
@books_blueprint.route('/read_book', methods=['GET'])
@login_required
def read_book():
    user_name = session['user_name'] # gets user name of user currently in session
    book_id = int(request.args.get('book_id'))
    book = services.get_book(book_id, repo.repo_instance)
    services.add_to_readinglist(user_name, book_id, repo.repo_instance)
    return redirect(url_for('books_bp.browse_all', title=book.title, added=True))

class reviewForm(FlaskForm):
    review = TextAreaField('Write a review', [
        DataRequired(), 
        Length(min=4, message='Your review text is too short')])
    rating = RadioField('Rating out of 5:', choices=[(1,'1/5'), (2, '2/5'), (3, '3/5'), (4, '4/5'), (5, '5/5')]) # doesn't let you click submit unless this field is completed
    book_id = HiddenField("Book_id")
    submit = SubmitField("Submit review")
