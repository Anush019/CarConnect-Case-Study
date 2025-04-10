class Admin:
    def __init__(self, admin_id, first_name, last_name, email, phone, username, password, role, join_date):
        self.admin_id = admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.password = password
        self.role = role
        self.join_date = join_date

    def authenticate(self, input_password):
        return self.password == input_password
