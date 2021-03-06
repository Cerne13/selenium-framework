from pages.courses.checkout import Checkout
from utilities.test_status import Status
import unittest
import pytest
from ddt import ddt, data, unpack
from utilities.read_data import get_csv_data

@ddt
@pytest.mark.usefixtures('one_time_set_up', 'set_up')
class CheckoutTestCSV(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def class_setup(self, one_time_set_up):
        self.checkout = Checkout(self.driver)
        self.ts = Status(self.driver)

    def set_up(self):
        self.driver.find_element_by_xpath ("//a[contains(text(), 'Home')]").click ()

    @pytest.mark.run(order=1)
    @data(*get_csv_data('testdata.csv'))
    @unpack
    def test_checkout(self, first_name, second_name, address, city, postcode, phone, email):
        self.checkout.enter_item_name('Wooden Rocking Chair')
        self.checkout.click_search_btn()
        result = self.checkout.verify_item_page()
        self.ts.mark(result, 'We are on the wrong page')

        self.checkout.click_plus()
        self.checkout.click_add_to_cart()
        self.checkout.click_view_cart()
        cart_page_check = self.checkout.verify_cart_page()
        self.ts.mark_final('test_checkout', cart_page_check, 'We are not on the cart page')
        self.checkout.click_proceed()

        self.checkout.enter_credentials(first_name, second_name, address, city, postcode, phone, email)
        self.checkout.click_place_order()
        self.checkout.verify_checkout_fail()
        self.ts.mark_final('verify_checkout_fail', result, 'We did not get the error message')



