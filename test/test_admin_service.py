import unittest
from unittest.mock import MagicMock
from entity.admin import Admin
from dao.admin_service import AdminService

class TestAdminService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = AdminService(self.mock_db)

    def test_get_admin_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [("John", "Doe")]
        self.service.get_admin_by_id(1)
        self.mock_db.fetch_query.assert_called_once()

    def test_get_admin_by_username_valid(self):
        self.mock_db.fetch_query.return_value = [("admin1", "Admin")]
        self.service.get_admin_by_username("admin1")
        self.mock_db.fetch_query.assert_called_once()

    def test_register_admin_valid(self):
        admin = Admin("John", "Doe", "john@example.com", "1234567890", "admin1", "pass123", "Manager")
        self.service.register_admin(admin)
        self.mock_db.execute_query.assert_called_once()

    def test_update_admin_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_admin(1, "John", "Smith", "johnsmith@example.com", "9876543210", "johnsmith", "Admin")
        self.mock_db.execute_query.assert_called_once()

    def test_delete_admin_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.delete_admin(1)
        self.mock_db.execute_query.assert_called_once()

if __name__ == "__main__":
    unittest.main()
