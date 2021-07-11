import pytest

from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter, Retry

from os import path
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(log_file_path)
# logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("init conftest")

def test_auth_register(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/register')
    response = request_session.post(
        url=api_url+'api/register', 
        json={
            "email:" : "testemail11@gmail.com", "password": "1234absdABSD!"
    })
    assert response.status_code == 200


def test_auth_login(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login')
    response = request_session.post(
        url=api_url+'api/login', 
        json={
            "email:" : "testemail11@gmail.com", "password": "1234absdABSD!"
    })
    assert response.status_code == 200


def test_auth_login_wrong_email(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login wrong emain')
    response = request_session.post(
        url=api_url+'api/login', 
        json={
            "email:" : "testemail11", "password": "1234absdABSD!"
    })
    assert response.status_code == 422


def test_auth_login_used_email(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login used emain')
    response = request_session.post(
        url=api_url+'api/login', 
        json={
            "email:" : "testemail11@gmail.com", "password": "1234absdABSD!"
    })
    assert response.status_code == 422


def test_auth_login_wrong_password(wait_app_container):
    request_session, api_url = wait_app_container
    logger.info(f'request {api_url}api/login wrong password')
    response = request_session.post(
        url=api_url+'api/login', 
        json={
            "email:" : "testemail11", "password": "1234absd"
    })
    assert response.status_code == 422

