from base.basepage import BasePage
import utilities.logger as cl
import logging

class Checkout(BasePage):
    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _search_box = 'woocommerce-product-search-field-0'
    _search_button = "//div[@class='elementor-widget-container']//button[@type='submit']"
    _plus_button = "//a[text()='+']"
    _add_to_cart_button = "//button[contains(text(), 'Add to cart')]"
    _view_cart = "//form[@class='cart']//a[text()='View cart']"
    _proceed_to_checkout = '//a[contains(text(), "Proceed ")]'

    _first_name_field = 'billing_first_name'
    _second_name_field = 'billing_last_name'
    _address_field = 'billing_address_1'
    _city_field = 'billing_city'
    _postcode_field = 'billing_postcode'
    _phone_field = 'billing_phone'
    _email_field = 'billing_email'

    _place_order = 'place_order'

    _checkout_error_message = "//li[contains(text(), 'Invalid payment')]"

    def enter_item_name(self, name):
        self.element_send_keys(name, self._search_box)

    def click_search_btn(self):
        self.element_click(self._search_button, 'xpath')

    def verify_item_page(self):
        result = self.is_element_present("//h1[contains(text(), 'Rocking Chair')]", 'xpath')
        return result

    def click_plus(self):
        self.element_click(self._plus_button, 'xpath')

    def click_add_to_cart(self):
        self.element_click(self._add_to_cart_button, 'xpath')

    def click_view_cart(self):
        self.wait_for_element(self._view_cart, 'xpath')
        self.element_click(self._view_cart, 'xpath')

    def verify_cart_page(self):
        result = 'Cart' in self.get_title()
        return result

    def click_proceed(self):
        self.element_click(self._proceed_to_checkout, 'xpath')

    def enter_credentials(self, first_name, second_name, address, city, postcode, phone, email):
        self.element_send_keys(first_name, self._first_name_field)
        self.element_send_keys(second_name, self._second_name_field)
        self.element_send_keys(address, self._address_field)
        self.element_send_keys(city, self._city_field)
        self.element_send_keys(postcode, self._postcode_field)
        self.element_send_keys(phone, self._phone_field)
        self.element_send_keys(email, self._email_field)

    def click_place_order(self):
        self.element_click(self._place_order)

    def verify_checkout_fail(self):
        message_element = self.wait_for_element(self._checkout_error_message, 'xpath')
        result = self.is_element_displayed(message_element)
        return result
