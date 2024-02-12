import logging
import allure
import curlify
import requests
from allure_commons.types import AttachmentType
from allure_commons._allure import step
from tests.conftest import API_URL


def post_demowebshop(url, **kwargs):
    with step(f'POST {url}'):
        response = requests.post(API_URL + url, **kwargs)
        curl = curlify.to_curl(response.request)
        logging.info(curl)
        allure.attach(body=curl, name='curl', attachment_type=AttachmentType.TEXT, extension='txt')
    return response

