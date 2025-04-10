import unittest
from unittest.mock import patch, MagicMock
from CarConnect.dao.customer_service import CustomerService
from CarConnect.exceptions.authentication_exception import AuthenticationException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException

class TestCustomerAuthentication(unittest.TestCase):
    def setUp(self):
        mock_db = MagicMock()
        self.customer_service = CustomerService(mock_db)

    @patch('builtins.input', side_effect=["meens", "meens"])
    def test_authentication_with_user_input(self, mock_inputs):
        username = input("Enter username: ")
        password = input("Enter password: ")
        try:
            self.customer_service.authenticate_customer(username, password)
            print("Authentication successful")
        except (AuthenticationException, InvalidInputException) as e:
            print(f"Authentication failed: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @patch('builtins.input', side_effect=["1", "newemail@example.com", "1234567890", "New Address"])
    def test_update_customer_info_with_input(self, mock_inputs):
        try:
            customer_id = int(input("Enter customer ID: "))
            email = input("Enter new email: ")
            phone = input("Enter new phone: ")
            address = input("Enter new address: ")
            self.customer_service.update_customer(customer_id, email, phone, address)
            print("Customer info updated")
        except InvalidInputException as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Update failed: {e}")

if __name__ == '__main__':
    unittest.main()
