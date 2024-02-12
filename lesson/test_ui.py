import requests
from selene import browser, have

from allure_commons._allure import step

LOGIN = "example1200@example.com"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_with_api():
    """Successful authorization to some demowebshop (UI)"""
    response = requests.post(API_URL + '/login', data={'Email': LOGIN, 'Password': PASSWORD, 'RememberMe': True}, allow_redirects=False)
    assert response.status_code == 302
    cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with step("Open main page with authorized user"):
        browser.open("http://demowebshop.tricentis.com/")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("http://demowebshop.tricentis.com/")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))
