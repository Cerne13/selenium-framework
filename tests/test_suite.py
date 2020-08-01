import unittest
from tests.checkout.checkout_test import CheckoutTest
from tests.checkout.checkout_test_csv_data import CheckoutTestCSV

tc1 = unittest.TestLoader().loadTestsFromTestCase(CheckoutTestCSV)
tc2 = unittest.TestLoader().loadTestsFromTestCase(CheckoutTest)

smoke_test = unittest.TestSuite([tc1, tc2])

unittest.TextTestRunner(verbosity=2).run(smoke_test)
