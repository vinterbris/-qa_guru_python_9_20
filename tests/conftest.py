import os

import dotenv
import pytest
import requests
from selene import browser
from selenium import webdriver

API_URL = "https://demowebshop.tricentis.com/"


@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.window_width = 1600
    browser.config.window_height = 900
    browser.config.base_url = 'http://demowebshop.tricentis.com'
    driver_options = webdriver.ChromeOptions()
    browser.config.driver_options = driver_options

    yield

    browser.element('.cart-label').click()
    for i in range(len(browser.all('[name=removefromcart]'))):
        browser.all('[name=removefromcart]')[i].click()
    browser.element('.update-cart-button').click()

    browser.quit()


@pytest.fixture(scope='function')
def get_login_cookie():
    dotenv.load_dotenv()
    response = requests.post(API_URL + '/login',
                             data={'Email': os.getenv('LOGIN'), 'Password': os.getenv('PASSWORD'), 'RememberMe': True},
                             allow_redirects=False)
    cookie_name = 'NOPCOMMERCE.AUTH'
    cookie = response.cookies.get(cookie_name)
    user_cookie = {'NOPCOMMERCE.AUTH': cookie}

    yield cookie, cookie_name
