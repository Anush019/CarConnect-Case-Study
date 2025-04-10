class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone, address, username, password, registration_date):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.username = username
        self.password = password
        self.registration_date = registration_date

    def authenticate(self, input_password):
        return self.password == input_password
