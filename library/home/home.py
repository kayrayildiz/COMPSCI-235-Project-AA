from flask import Blueprint, render_template

import library.utilities.utilities as utilities


home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    books = utilities.get_books_by_title()
    return render_template(
        'home/home.html',
        books = books
    ) 
