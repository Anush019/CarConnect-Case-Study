import unittest
from unittest.mock import MagicMock
from datetime import date
from dao.customer_service import CustomerService
from entity.customer import Customer
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.customer_not_found_exception import CustomerNotFoundException
from exceptions.authentication_exception import AuthenticationException

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = CustomerService(self.mock_db)

    def test_get_customer_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [("1", "John", "Doe", "john@example.com", "1234567890", "Address", "johndoe", "pass123", date.today())]
        self.service.get_customer_by_id("1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_customer_by_id_invalid(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_customer_by_id("abc")

    def test_get_customer_by_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(CustomerNotFoundException):
            self.service.get_customer_by_id("999")

    def test_get_customer_by_username_valid(self):
        self.mock_db.fetch_query.return_value = [("1", "John", "Doe", "john@example.com", "1234567890", "Address", "johndoe", "pass123", date.today())]
        self.service.get_customer_by_username("johndoe")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_customer_by_username_invalid(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_customer_by_username("")

    def test_get_customer_by_username_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(CustomerNotFoundException):
            self.service.get_customer_by_username("unknown_user")

    def test_register_customer_valid(self):
        customer = Customer(None, "Jane", "Doe", "jane@example.com", "1234567890", "Somewhere", "janedoe", "securepass", None)
        self.service.register_customer(customer)
        self.mock_db.execute_query.assert_called_once()

    def test_register_customer_invalid_phone(self):
        customer = Customer(None, "Jane", "Doe", "jane@example.com", "12345abc", "Somewhere", "janedoe", "securepass", None)
        with self.assertRaises(InvalidInputException):
            self.service.register_customer(customer)

    def test_register_customer_empty_fields(self):
        customer = Customer(None, "", "Doe", "jane@example.com", "1234567890", "Somewhere", "janedoe", "securepass", None)
        with self.assertRaises(InvalidInputException):
            self.service.register_customer(customer)

    def test_update_customer_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_customer("1", "Jane", "Doe", "jane@example.com", "1234567890", "Somewhere", "janedoe")
        self.mock_db.execute_query.assert_called_once()

    def test_update_customer_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_customer("abc", "Jane", "Doe", "jane@example.com", "1234567890", "Somewhere", "janedoe")

    def test_update_customer_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(CustomerNotFoundException):
            self.service.update_customer("99", "Jane", "Doe", "jane@example.com", "1234567890", "Somewhere", "janedoe")

    def test_delete_customer_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.delete_customer("1")
        self.mock_db.execute_query.assert_called_once()

    def test_delete_customer_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.delete_customer("abc")

    def test_delete_customer_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(CustomerNotFoundException):
            self.service.delete_customer("99")

    def test_authenticate_customer_valid(self):
        self.mock_db.fetch_query.return_value = [("1", "Jane")]
        self.service.authenticate_customer("janedoe", "securepass")
        self.mock_db.fetch_query.assert_called_once()

    def test_authenticate_customer_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.authenticate_customer("", "password")
        with self.assertRaises(InvalidInputException):
            self.service.authenticate_customer("username", "")

    def test_authenticate_customer_failure(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(AuthenticationException):
            self.service.authenticate_customer("janedoe", "wrongpass")

if __name__ == '__main__':
    unittest.main()
