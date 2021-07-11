import pytest

from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter, Retry

def test_spammers_create(make_spammers, wait_app_container):
    request_session, api_url = wait_app_container
    print(request_session, api_url)
    response = request_session.post(url=api_url+'api/spammers/', json=make_spammers)
    print(make_spammers)
    assert response.status_code == 200