import pytest
from base.webdriverfactory import WebDriverFactory
from pages.courses.checkout import Checkout

@pytest.fixture(scope='class')
def set_up():
    print('Running conftest demo setup')
    yield
    print('Running conftest demo teardown')


# scope was 'module' before we tested class

@pytest.fixture(scope='class')
def one_time_set_up(request, browser):
    print('Running one time conftest demo setup')

    wdf = WebDriverFactory(browser)
    driver = wdf.get_webdriver_instance()
    checkout = Checkout(driver)
    checkout.element_presence_check('woocommerce-product-search-field-0')

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    print('Running one time conftest teardown')


def pytest_addoption(parser):
    parser.addoption('--browser')
    parser.addoption('--os_type', help='Type of operating system')

@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption('--browser')

@pytest.fixture(scope='session')
def os_type(request):
    return request.config.getoption('--os_type')
