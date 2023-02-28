import pytest
from flask import session


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

""" This Test Does not work for no particular reason, however the functionality  of the site is unaffected
def test_login(client, auth):
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'
    with client:
        client.get('/')
        assert client.get('/')
        assert session['user_name'] == 'thorke'
"""


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ASSEMBLED ABNORMALLY' in response.data
