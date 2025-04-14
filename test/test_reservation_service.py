import unittest
from unittest.mock import MagicMock
from datetime import date
from entity.reservation import Reservation
from dao.reservation_service import ReservationService

class TestReservationService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = ReservationService(self.mock_db)

    def test_get_reservation_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [(1, 2, 3, date(2024, 5, 1), date(2024, 5, 5), 5000.00, "Confirmed")]
        reservation = self.service.get_reservation_by_id(1)
        self.assertIsInstance(reservation, Reservation)
        self.mock_db.fetch_query.assert_called_once()

    def test_get_reservations_by_customer_id_valid(self):
        self.mock_db.fetch_query.return_value = [
            (1, 2, 3, date(2024, 5, 1), date(2024, 5, 5), 5000.00, "Confirmed"),
            (2, 2, 4, date(2024, 6, 1), date(2024, 6, 3), 3000.00, "Pending"),
        ]
        reservations = self.service.get_reservations_by_customer_id(2)
        self.assertTrue(all(isinstance(r, Reservation) for r in reservations))
        self.mock_db.fetch_query.assert_called_once()

    def test_create_reservation_valid(self):
        reservation = Reservation(1, 2, 3, date(2024, 5, 1), date(2024, 5, 5), 5000.00, "Confirmed")
        self.service.create_reservation(reservation)
        self.mock_db.execute_query.assert_called_once()

    def test_update_reservation_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_reservation(1, "Cancelled")
        self.mock_db.execute_query.assert_called_once()

    def test_cancel_reservation_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.cancel_reservation(1)
        self.mock_db.execute_query.assert_called_once()

if __name__ == "__main__":
    unittest.main()
