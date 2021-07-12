from _pytest.fixtures import fixture
import pytest
from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter

from os import path, getenv
from dotenv import load_dotenv
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(log_file_path)
# logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def wait_app_container():
    load_dotenv()
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))
    print('start connect to "web" container')
    app_server = getenv('APP_SERVER')
    app_port = getenv('APP_PORT')
    print(app_server, app_port)
    assert app_server
    assert app_port
    api_url = f'http://{app_server}:{app_port}/'
    print(f'start request url {api_url}docs')

    assert request_session.get(f'{api_url}docs')
    return request_session, api_url


@pytest.fixture
def clear_spammers(wait_app_container):
    request_session, api_url = wait_app_container
    print(request_session, api_url)
    response = request_session.delete(url=api_url+'api/spammers/', json=[])
    print(make_spammers)
    print(response.json())
    assert response.status_code == 200



@pytest.fixture(scope="function")
def make_spammers():
    return [
        {
          "spammer_type": "111",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
        {
          "spammer_type": "222",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
        {
          "spammer_type": "333",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
]

@pytest.fixture
def make_stored_spammers():
    return [
        {
          "id": 39,
          "spammer_type": "111",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
        {
          "id": 40,
          "spammer_type": "222",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
        {
          "id": 41,
          "spammer_type": "333",
          "login": "string",
          "target": {
            "target_type": "string",
            "current": 0,
            "total": 0
          },
          "state": "stopped"
        },
]
