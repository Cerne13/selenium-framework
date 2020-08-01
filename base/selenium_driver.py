from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.logger as cl
import logging
import time
import os

class SeleniumDriver:

    log = cl.CustomLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenshot(self, result_message):
        filename = f'{result_message}.{str(round(time.time() * 1000))}.png'
        screenshot_dir = '..\\screenshots\\'
        relative_filename = screenshot_dir + filename
        current_dir = os.path.dirname(__file__)
        destination_file = os.path.join(current_dir, relative_filename)
        destination_dir = os.path.join(current_dir, screenshot_dir)

        try:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            self.driver.save_screenshot(destination_file)
            self.log.info(f'Screenshot saved to: {destination_file} ')
        except:
            self.log.error('Exception occurred')
            print_stack()

    def get_title(self):
        return self.driver.title

    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == 'id':
            return By.ID
        elif locator_type == 'xpath':
            return By.XPATH
        elif locator_type == 'name':
            return By.NAME
        elif locator_type == 'css':
            return By.CSS_SELECTOR
        elif locator_type == 'class':
            return By.CLASS_NAME
        elif locator_type == 'link':
            return By.LINK_TEXT
        else:
            self.log.info('Locator' + locator_type + 'not supported')
        return False

    def get_element(self, locator, locator_type='id'):
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info(f'Element found with locator {locator} and locator type {locator_type}')
        except:
            self.log.info('Element not found')
        return element

    def get_element_list(self, locator, locator_type='id'):
        elements = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            elements = self.driver.find_elements(by_type, locator)
            self.log.info(f'Element found with locator {locator} and locator type {locator_type}')
        except:
            self.log.info(f'No elements with locator {locator} and locator type {locator_type} found')
        return elements

    def element_click(self, locator, locator_type='id', element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info(f'Clicked the element with locator: {locator}, locator type: {locator_type}.')
        except:
            self.log.info(f"Can't click the element with locator: {locator}, locator type: {locator_type}.")
            print_stack()

    def element_send_keys(self, data, locator, locator_type='id', element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(f'Sent data to the element with locator: {locator}, locator type: {locator_type}.')
        except:
            self.log.info(f"Can't sent data to the element with locator: {locator}, locator type: {locator_type}.")
            print_stack()

    def get_text(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                self.log.debug("In locator condition")
                element = self.get_element(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " +  info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def is_element_present(self, locator='', locator_type='id', element=None):
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info(f'Element found with locator {locator} and locator type {locator_type}')
                return True
            else:
                self.log.info (f'Element with locator {locator} and locator type {locator_type} not found')
                return False
        except:
            self.log.info('Exception occured')
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        is_displayed = False
        try:
            if locator:
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " locatorType: " + locator_type)
            else:
                self.log.info("Element not displayed with locator: " + locator +
                              " locatorType: " + locator_type)
            return is_displayed
        except:
            print("Element not found")
            return False

    def element_presence_check(self, locator, locator_type='id'):
        try:
            element_list = self.driver.find_elements(locator_type, locator)
            if len(element_list) > 0:
                self.log.info('Element found')
                return True
            else:
                return False
        except:
            self.log.info('Element not found')
            return False

    def wait_for_element(self, locator, locator_type="id",
                         timeout=10, pollFrequency=0.5):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def web_scroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")
