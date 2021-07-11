import pytest
from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter

from os import path
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(log_file_path)
# logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("init conftest")

pytest_plugins = ["docker_compose"]

@pytest.fixture(scope="module")
def wait_app_container(module_scoped_container_getter):
    print('start wait "web" container fixture')
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))
    print('start connect to "web" container')
    service = module_scoped_container_getter.get("web").network_info[0]
    print(f'connected to "web" container with info: {service}')
    api_url = f'http://{service.hostname}:{service.host_port}/'
    print(f'start request url {api_url}docs')
    assert request_session.get(f'{api_url}docs')
    print(f'successfull request')
    return request_session, api_url

@pytest.fixture(scope="function")
def make_spammers():
    print('start make spammers')
    return [
    {
        "spammer_type": "vk",
        "login": "1111",
        "target": {
            "target_type": "post",
            "current": 0,
            "total": 0
        },
        "state": "working"
    },
    {
        "s_type": "vk",
        "login": "1111",
        "target": {
            "t_type": "post",
            "current": 0,
            "total": 0
        },
        "state": "working"
    },
    {
        "s_type": "vk",
        "login": "1111",
        "target": {
            "t_type": "post",
            "current": 0,
            "total": 0
        },
        "state": "working"
    }
]

