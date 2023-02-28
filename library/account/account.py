from wtforms.widgets.core import CheckboxInput
from library.adapters.memory_repository import MemoryRepository
from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import library.adapters.repository as repo
import library.utilities.utilities as utilities
import library.utilities.services as services

from library.authentication.authentication import login_required 
from library.domain.model import Review, Book, User

account_blueprint = Blueprint('account_bp', __name__)

@account_blueprint.route('/my_account', methods=['GET'])
def view_account():
    user_name = session['user_name']
    reading_list = services.get_readinglist_for_user(user_name, repo.repo_instance)
    reading_list_urls = utilities.get_readinglist_urls(reading_list)
    
    select_urls = services.get_recommended_books(reading_list, repo.repo_instance)
    return render_template(
        'account/account.html', 
        reading_list = reading_list, 
        reading_list_urls = reading_list_urls, 
        include_recommendations = True, 
        select_urls = select_urls
    )

