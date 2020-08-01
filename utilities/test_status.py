from base.selenium_driver import SeleniumDriver
import logging
import utilities.logger as cl


class Status(SeleniumDriver):
    log = cl.CustomLogger(logging.INFO)

    def __init__(self, driver):
        # just user super().__init__ instead of super(TestStatus, self).__init__
        super().__init__(driver)
        self.result_list = []

    def set_result(self, result, message):
        try:
            if result is not None:
                if result:
                    self.result_list.append('PASS')
                    self.log.info(f'*** VERIFICATION SUCCESSFUL: {message}')
                else:
                    self.result_list.append('FAIL')
                    self.log.error(f'!!! VERIFICATION FAILED: {message}')
                    self.screenshot(message)
            else:
                self.result_list.append('FAIL')
                self.log.error(f'!!! VERIFICATION FAILED: {message}')
                self.screenshot(message)
        except:
            self.result_list.append('FAIL')
            self.screenshot(message)
            self.log.error('---EXCEPTION OCCURED')

    def mark(self, result, message):
        self.set_result(result, message)

    def mark_final(self, test_name, result, message):
        self.set_result(result, message)

        if 'FAIL' in self.result_list:
            self.log.error(f'!!! {test_name} has failed!')
            self.result_list.clear()
            assert True == False
        else:
            self.log.info(f'*** {test_name} was successful')
            self.result_list.clear()
            assert True == True
