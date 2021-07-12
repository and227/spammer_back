import pytest

from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter, Retry

from os import path
import logging.config
import json

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(log_file_path)
# logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("init conftest")

pytest.test_email = "testemaild99@gmail.com"
pytest.test_password = "1234absdABSD!"


def test_auth_register(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/register')
    headers = {'Content-type': 'application/json'}
    response = request_session.post(
        url=api_url+'api/register', 
        data=json.dumps({
            "email" : pytest.test_email,
            "password": pytest.test_password
        }),
        headers=headers
    )
    assert response.status_code == 200


def test_auth_login(wait_app_container):
    request_session, api_url = wait_app_container
    print(f'request {api_url}api/login')
    headers = {'Content-type': 'application/json'}
    response = request_session.post(
        url=api_url+'api/login', 
        data=json.dumps({
            "email" : pytest.test_email,
            "password": pytest.test_password
        }),
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200


def test_auth_login_wrong_email(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login wrong emain')
    headers = {'Content-type': 'application/json'}
    response = request_session.post(
        url=api_url+'api/login', 

        data=json.dumps({
            "email" : pytest.test_email + '111',
            "password": pytest.test_password
        }),
        headers=headers
    )
    assert response.status_code == 422


def test_auth_login_wrong_password(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login wrong password')
    headers = {'Content-type': 'application/json'}
    response = request_session.post(
        url=api_url+'api/login', 
        data=json.dumps({
            "email" : pytest.test_email,
            "password": 'some_pass'
        }),
        headers=headers
    )
    assert response.status_code == 401


def test_auth_login_register_used_email(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/register used emain')
    headers = {'Content-type': 'application/json'}
    response = request_session.post(
        url=api_url+'api/register', 
        data=json.dumps({
            "email" : pytest.test_email,
            "password": pytest.test_password
        }),
        headers=headers
    )
    assert response.status_code == 422


def test_delete_user(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/user_delete')
    headers = {'Content-type': 'application/json'}
    response = request_session.delete(
        url=api_url+'api/user_delete', 
        data=json.dumps({
            "email" : pytest.test_email,
            "password": pytest.test_password
        }),
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200