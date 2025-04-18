import unittest
from unittest.mock import MagicMock
from dao.vehicle_service import VehicleService
from entity.vehicle import Vehicle
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.vehicle_not_found_exception import VehicleNotFoundException
from exceptions.database_connection_exception import DatabaseConnectionException

class TestVehicleService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = VehicleService(self.mock_db)


    def test_get_vehicle_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [(1, "ModelX", "Tesla", "2023", "Red", "TS12B1234", 1, 3500)]
        self.service.get_vehicle_by_id("1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_vehicle_by_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(VehicleNotFoundException):
            self.service.get_vehicle_by_id("999")

    def test_get_vehicle_by_id_db_error(self):
        self.mock_db.fetch_query.side_effect = DatabaseConnectionException("DB down")
        with self.assertRaises(DatabaseConnectionException):
            self.service.get_vehicle_by_id("1")


    def test_get_available_vehicles_success(self):
        self.mock_db.fetch_query.return_value = [
            (1, "ModelX", "Tesla", "2023", "Red", "TS12AB1234", 1, 3500)
        ]
        vehicles = self.service.get_available_vehicles()
        self.assertIsInstance(vehicles, list)

    def test_get_available_vehicles_db_error(self):
        self.mock_db.fetch_query.side_effect = DatabaseConnectionException("DB error")
        with self.assertRaises(DatabaseConnectionException):
            self.service.get_available_vehicles()


    def test_add_vehicle_valid(self):
        vehicle = Vehicle(None, "Model3", "Tesla", "2023", "Blue", "TN12C3456", "1", 4500)
        self.service.add_vehicle(vehicle)
        self.mock_db.execute_query.assert_called_once()

    def test_add_vehicle_invalid_registration(self):
        vehicle = Vehicle(None, "Model3", "Tesla", "2023", "Blue", "INVALID", "1", 4500)
        with self.assertRaises(InvalidInputException):
            self.service.add_vehicle(vehicle)

    def test_add_vehicle_invalid_year(self):
        vehicle = Vehicle(None, "Model3", "Tesla", "23", "Blue", "TN12C3456", "1", 4500)
        with self.assertRaises(InvalidInputException):
            self.service.add_vehicle(vehicle)

    def test_add_vehicle_db_exception(self):
        vehicle = Vehicle(None, "Model3", "Tesla", "2023", "Blue", "TN12B3456", "1", 4500)
        self.mock_db.execute_query.side_effect = Exception("Insert failed")
        with self.assertRaises(DatabaseConnectionException):
            self.service.add_vehicle(vehicle)


    def test_update_vehicle_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_vehicle("1", "3000", "1")
        self.mock_db.execute_query.assert_called_once()

    def test_update_vehicle_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_vehicle("abc", "3000", "1")

    def test_update_vehicle_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(VehicleNotFoundException):
            self.service.update_vehicle("999", "3000", "1")

    def test_update_vehicle_db_exception(self):
        self.mock_db.execute_query.side_effect = DatabaseConnectionException("Update failed")
        with self.assertRaises(DatabaseConnectionException):
            self.service.update_vehicle("1", "3000", "1")


    def test_remove_vehicle_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.remove_vehicle("1")
        self.mock_db.execute_query.assert_called_once()

    def test_remove_vehicle_invalid_id(self):
        with self.assertRaises(InvalidInputException):
            self.service.remove_vehicle("xyz")

    def test_remove_vehicle_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(VehicleNotFoundException):
            self.service.remove_vehicle("999")

    def test_remove_vehicle_db_exception(self):
        self.mock_db.execute_query.side_effect = DatabaseConnectionException("Delete failed")
        with self.assertRaises(DatabaseConnectionException):
            self.service.remove_vehicle("1")

if __name__ == "__main__":
    unittest.main()
