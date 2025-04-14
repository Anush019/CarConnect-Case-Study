import unittest
from unittest.mock import MagicMock
from entity.vehicle import Vehicle
from dao.vehicle_service import VehicleService
from exceptions.vehicle_not_found_exception import VehicleNotFoundException

class TestVehicleService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_db.fetch_query.return_value = [
            (1, "Tesla", "Model S", 2023, "Black", "TS1234", 1, 3500.50, 1),
            (2, "Toyota", "Camry", 2022, "White", "TN9876", 1, 2500.00, 1)
        ]
        self.service = VehicleService(self.mock_db)

    def test_add_vehicle(self):
        vehicle = Vehicle(1, "Tesla", "Model S", 2023, "Black", "TS1234", 1, 3500.50)
        try:
            self.service.add_vehicle(vehicle)
            print("Vehicle added successfully.")
        except Exception as e:
            self.fail(f"Vehicle addition failed: {e}")

    def test_update_vehicle(self):
        try:
            self.service.update_vehicle(1, 4000.00, 0)
            print("Vehicle updated successfully.")
        except Exception as e:
            self.fail(f"Vehicle update failed: {e}")

    def test_get_available_vehicles(self):
        try:
            vehicles = self.service.get_available_vehicles()
            self.assertIsInstance(vehicles, list)
            print("Available vehicles fetched successfully.")
        except VehicleNotFoundException:
            print("No available vehicles found.")
        except Exception as e:
            self.fail(f"Fetching available vehicles failed: {e}")

if __name__ == "__main__":
    unittest.main()
