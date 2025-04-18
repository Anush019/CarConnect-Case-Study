from entity.customer import Customer
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.authentication_exception import AuthenticationException
from exceptions.customer_not_found_exception import CustomerNotFoundException
from tabulate import tabulate

class CustomerService():
    def __init__(self, db):
        self.db = db

    def get_customer_by_id(self, customer_id):
        if not customer_id.isdigit():
            raise InvalidInputException("Customer ID must be an integer.")

        query = "SELECT * FROM Customer WHERE CustomerID = %s"
        result = self.db.fetch_query(query, (customer_id,))

        if not result:
            raise CustomerNotFoundException(f"Customer with ID '{customer_id}' not found.")


        customer_data = result[0]
        display_data = [customer_data[0], customer_data[1], customer_data[3], customer_data[4],
                        customer_data[8]]
        headers = ["CustomerID", "Name", "Email", "Phone", "RegistrationDate"]

        print(tabulate([display_data], headers=headers, tablefmt="fancy_grid"))

    def get_customer_by_username(self, username):
        if not isinstance(username, str) or not username.strip():
            raise InvalidInputException("Username must be a non-empty string.")

        query = "SELECT * FROM Customer WHERE Username = %s"
        result = self.db.fetch_query(query, (username,))

        if not result:
            raise CustomerNotFoundException(f"Customer with username '{username}' not found.")

        customer_data = result[0]
        display_data = [customer_data[0], customer_data[1], customer_data[3], customer_data[4],
                        customer_data[8]]
        headers = ["CustomerID", "Name", "Email", "Phone", "RegistrationDate"]

        print(tabulate([display_data], headers=headers, tablefmt="fancy_grid"))

    def register_customer(self, customer):
        if not all([customer.first_name.strip(),customer.last_name.strip(),customer.email.strip(),
                    customer.address.strip(), customer.username.strip(),customer.password.strip()]):
            raise InvalidInputException("Fields must not be empty.")

        if not (customer.phone.isdigit() and len(customer.phone) == 10):
            raise InvalidInputException("Phone number must be a 10-digit number.")

        query = """
            INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber, Address, Username, Password, RegistrationDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        self.db.execute_query(query, (
            customer.first_name, customer.last_name, customer.email,
            customer.phone, customer.address, customer.username, customer.password
        ))

    def update_customer(self, customer_id,first_name,last_name ,email, phone, address,username):
        if not customer_id.isdigit():
            raise InvalidInputException("Customer ID must be an integer.")
        query = """
            UPDATE Customer SET firstname = %s,lastname = %s,
            Email = %s, PhoneNumber = %s, Address = %s,username = %s WHERE CustomerID = %s
        """
        result = self.db.execute_query(query, (first_name,last_name,email, phone, address,username,customer_id))
        if result == 0:
            raise CustomerNotFoundException(f"Customer ID {customer_id} not found")

    def delete_customer(self, customer_id):
        if not customer_id.isdigit():
            raise InvalidInputException("Customer ID must be an integer.")
        query = "DELETE FROM Customer WHERE CustomerID = %s"
        result = self.db.execute_query(query, (customer_id,))
        if result == 0:
            raise CustomerNotFoundException(f"Customer ID {customer_id} not found")

    def authenticate_customer(self, username, password):
        if not isinstance(username, str) or not username.strip():
            raise InvalidInputException("Username must be a non-empty string.")
        if not isinstance(password, str) or not password.strip():
            raise InvalidInputException("Password must be a non-empty string.")


        query = "SELECT CustomerID, FirstName FROM Customer WHERE Username = %s AND Password = %s"
        result = self.db.fetch_query(query, (username, password))

        if not result:
            raise AuthenticationException("Invalid username or password.")

        customer_id, first_name = result[0]

        print("Successfully logged in!")
        print(f"Welcome, {first_name} (Customer ID: {customer_id})")



