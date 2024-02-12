import logging
import os

import allure
import curlify
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType

from lesson import schemas

from lesson.schema import load
from jsonschema import validate

SCHEMA_INIT = os.path.abspath(schemas.__file__)  # происходит ссылка на __init__, который никуда не денется
SCHEMA_DIR = os.path.dirname(SCHEMA_INIT)
BASE_URL = 'https://reqres.in'


def post_reqres(url, **kwargs):
    base_url = 'https://reqres.in'
    with step(f'POST {url}'):
        response = requests.post(base_url + url, kwargs)
        curl = curlify.to_curl(response.request)
        logging.info(curl)
        allure.attach(body=curl, name='curl', attachment_type=AttachmentType.TEXT, extension='txt')
    return response


def test_list_users_validate_schema_with_post_reqres():
    response = post_reqres('/api/users?page=2')
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "get_users_list.json")
    validate(body, schema=load(schema))


def test_list_users_validate_schema():
    response = requests.get(BASE_URL + '/api/users?page=2')
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "get_users_list.json")
    validate(body, schema=load(schema))
