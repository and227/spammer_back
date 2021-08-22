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
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "stopped",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          }
        },
        {
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "stopped",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          }
        },
        {
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "stopped",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          }
        },
]

@pytest.fixture
def make_stored_spammers():
    return [
        {
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "working",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          },
          "id": 18,
          "statistics": {
            "total": 0,
            "current": 15
          }
        },
        {
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "working",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          },
          "id": 18,
          "statistics": {
            "total": 0,
            "current": 15
          }
        },
        {
          "script_template": "string",
          "login": "string",
          "password": "string",
          "state": "working",
          "options": {
            "opt1": 1,
            "opt2": "value",
            "opt3": [1,2,3,4,5]
          },
          "id": 18,
          "statistics": {
            "total": 0,
            "current": 15
          }
        }
    ]
