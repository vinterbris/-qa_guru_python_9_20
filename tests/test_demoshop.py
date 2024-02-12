from selene import browser, have

from allure_commons._allure import step
from tests.conftest import API_URL
from utils.logger import post_demowebshop


def test_check_adding_item_into_cart(get_login_cookie):
    cookie, cookie_name = get_login_cookie
    with step("Open main page with authorized user"):
        browser.open('/')
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open("/")

    with step("Add single item to cart through api"):
        post_demowebshop('addproducttocart/catalog/45/1/1', cookies={cookie_name: cookie})
    with step("Validate items and amount in cart through ui"):
        browser.element('.cart-label').click()
        browser.all('.product-name').should(have.texts('Fiction'))
        browser.element('.qty-input').should(have.value('1'))


def test_check_adding_multipe_same_items_into_cart(get_login_cookie):
    cookie, cookie_name = get_login_cookie
    amount_of_items = 10000
    with step("Open main page with authorized user"):
        browser.open('/')
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open("/")

    with step("Add single item to cart through api"):
        post_demowebshop('addproducttocart/details/45/1',
                         data={'addtocart_45.EnteredQuantity': amount_of_items}, cookies={cookie_name: cookie})
    with step("Validate items and amount in cart through ui"):
        browser.element('.cart-label').click()
        browser.all('.product-name').should(have.texts('Fiction'))
        browser.element('.qty-input').should(have.value(f'{amount_of_items}'))


def test_check_adding_multiple_items_into_cart(get_login_cookie):
    cookie, cookie_name = get_login_cookie
    with step("Open main page with authorized user"):
        browser.open('/')
        browser.driver.add_cookie({"name": cookie_name, "value": cookie})
        browser.open("/")

    with step("Add single item to cart through api"):
        post_demowebshop('addproducttocart/catalog/45/1/1', cookies={cookie_name: cookie})
        post_demowebshop('addproducttocart/catalog/13/1/1', cookies={cookie_name: cookie})
        post_demowebshop('addproducttocart/catalog/22/1/1', cookies={cookie_name: cookie})
    with step("Validates item and amount in cart through ui"):
        browser.element('.cart-label').click()
        browser.all('.product-name').should(have.texts('Fiction', 'Computing and Internet', 'Health Book'))
        browser.all('.qty-input').should(have.values('1', '1', '1'))
