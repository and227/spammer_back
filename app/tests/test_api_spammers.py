from fastapi import params
from pydantic.types import Json
import pytest

from urllib.parse import urljoin
from requests import api
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter, Retry


def check_spammers(spammers_sample, spammers_checked):
    print('make:', spammers_sample)
    print('data:', spammers_checked)
    spammers_sample = sorted(spammers_sample, key=lambda s: s['script_template'])
    spammers_checked = sorted(spammers_checked, key=lambda s: s['script_template'])
    try:
        for spammer1, spammer2 in zip(spammers_checked, spammers_sample):
            if spammer1['script_template'] != spammer2['script_template'] \
            or spammer1['login'] != spammer2['login'] \
            or spammer1['password'] != spammer2['password'] \
            or spammer1['options'] != spammer2['options'] \
            or spammer1['id'] is None:
                return False
    except KeyError:
        return False

    pytest.test_spammer_id = spammers_checked[0]['id']
    return True


def check_spammers_start(spammers_checked):
    try:
        for spammer in spammers_checked:
            print('spam', spammer)
            if spammer['state'] != 'working':
                return False
    except KeyError:
        return False

    return True


def check_spammers_stop(spammers_checked):
    try:
        for spammer in spammers_checked:
            if spammer['state'] != 'stopped':
                return False
    except KeyError:
        return False

    return True


def test_spammers_create(wait_app_container, clear_spammers, make_spammers):
    request_session, api_url = wait_app_container
    print(request_session, api_url)
    response = request_session.post(url=api_url+'api/spammers/', json=make_spammers)
    assert response.status_code == 201


def test_spammers_get(wait_app_container, make_spammers):
    request_session, api_url = wait_app_container
    response = request_session.get(url=api_url+'api/spammers/', params={'offset': 0, 'limit': 10})
    assert response.status_code == 200
    assert check_spammers(make_spammers, response.json()['data'])


def test_spammers_get_status(wait_app_container, make_spammers):
    request_session, api_url = wait_app_container
    response = request_session.get(url=api_url+'api/spammers/status')
    print(response.json())
    assert check_spammers(make_spammers, response.json()['data'])


def test_spammers_status(wait_app_container, make_stored_spammers):
    request_session, api_url = wait_app_container
    response = request_session.get(url=api_url+'api/spammers/status/')
    assert check_spammers(make_stored_spammers, response.json()['data'])


def test_spammers_start(wait_app_container):
    request_session, api_url = wait_app_container
    request_session.put(url=api_url+'api/spammers/start/', json=[])

    response = request_session.get(url=api_url+'api/spammers/status/')
    assert check_spammers_start(response.json()['data'])


def test_spammers_stop(wait_app_container):
    request_session, api_url = wait_app_container
    request_session.put(url=api_url+'api/spammers/stop/', json=[])

    response = request_session.get(url=api_url+'api/spammers/status/')
    assert check_spammers_stop(response.json()['data'])


def test_spammers_start_detail(wait_app_container):
    request_session, api_url = wait_app_container
    print(pytest.test_spammer_id)
    request_session.put(url=api_url+'api/spammers/start/', json=[pytest.test_spammer_id])

    response = request_session.get(url=api_url+'api/spammers/status/', params={'spammer_data': pytest.test_spammer_id})
    print(response.json())
    assert check_spammers_start(response.json()['data'])


def test_spammers_stop_detail(wait_app_container):
    request_session, api_url = wait_app_container
    request_session.put(url=api_url+'api/spammers/stop/', json=[pytest.test_spammer_id])

    response = request_session.get(url=api_url+'api/spammers/status/', params={'spammer_data': pytest.test_spammer_id})
    assert check_spammers_stop(response.json()['data'])