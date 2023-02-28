from pathlib import Path

from library.adapters.repository import AbstractRepository
from library.adapters.data_importer import load_reviews, load_users, load_books_and_authors


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load users to repo
    load_users(data_path, repo)

    # Load books and authors into the repository.
    load_books_and_authors(data_path, repo, database_mode)
    
    # Load book reviews
    load_reviews(data_path, repo)
    

    
    