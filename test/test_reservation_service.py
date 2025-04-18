import unittest
from unittest.mock import MagicMock
from datetime import date
from entity.reservation import Reservation
from dao.reservation_service import ReservationService
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.reservation_exception import ReservationException

class TestReservationService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = ReservationService(self.mock_db)


    def test_get_reservation_by_id_valid(self):
        self.mock_db.fetch_query.return_value = [
            ("1", "2", "3", date(2024, 5, 1), date(2024, 5, 5), "5000.00", "Confirmed")]
        self.service.get_reservation_by_id("1")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_reservation_by_id_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_reservation_by_id("abc")

    def test_get_reservation_by_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(ReservationException):
            self.service.get_reservation_by_id("99")


    def test_get_reservations_by_customer_id_valid(self):
        self.mock_db.fetch_query.return_value = [
            ("1", "2", "3", date(2024, 5, 1), date(2024, 5, 5), "5000.00", "Confirmed"),
            ("2", "2", "4", date(2024, 6, 1), date(2024, 6, 3), "3000.00", "Pending"),
        ]
        self.service.get_reservations_by_customer_id("2")
        self.mock_db.fetch_query.assert_called_once()

    def test_get_reservations_by_customer_id_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.get_reservations_by_customer_id("abc")

    def test_get_reservations_by_customer_id_not_found(self):
        self.mock_db.fetch_query.return_value = []
        with self.assertRaises(ReservationException):
            self.service.get_reservations_by_customer_id("55")


    def test_create_reservation_valid(self):
        reservation = Reservation(
            None, "2", "3", "2024-05-01", "2024-05-05", "0.0", "Confirmed"
        )
        # Vehicle is available and daily rate is 1000.0
        self.mock_db.fetch_one.return_value = (1, 1000.0)
        self.service.create_reservation(reservation)
        self.mock_db.fetch_one.assert_called_once_with(
            "SELECT Availability, DailyRate FROM Vehicle WHERE VehicleID = %s", ("3",)
        )
        self.mock_db.execute_query.assert_called_once_with(
            """
            INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            ("2", "3", "2024-05-01", "2024-05-05", 4000.0, "Confirmed")
        )

    def test_create_reservation_invalid_customer_vehicle_id(self):
        reservation = Reservation(None, "abc", "3", date(2024, 5, 1), date(2024, 5, 5), "5000.00", "Confirmed")
        with self.assertRaises(InvalidInputException):
            self.service.create_reservation(reservation)


    def test_update_reservation_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.update_reservation("1", "Cancelled")
        self.mock_db.execute_query.assert_called_once()

    def test_update_reservation_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.update_reservation("abc", "Cancelled")

    def test_update_reservation_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(ReservationException):
            self.service.update_reservation("999", "Completed")


    def test_cancel_reservation_valid(self):
        self.mock_db.execute_query.return_value = 1
        self.service.cancel_reservation("1")
        self.mock_db.execute_query.assert_called_once()

    def test_cancel_reservation_invalid_input(self):
        with self.assertRaises(InvalidInputException):
            self.service.cancel_reservation("abc")

    def test_cancel_reservation_not_found(self):
        self.mock_db.execute_query.return_value = 0
        with self.assertRaises(ReservationException):
            self.service.cancel_reservation("999")


    def test_generate_reservation_history_report(self):
        self.mock_db.fetch_query.return_value = [
            (1, 2, 3, date(2024, 5, 1), date(2024, 5, 5), "Confirmed")
        ]
        self.service.generate_reservation_history_report()
        self.mock_db.fetch_query.assert_called_once()


    def test_generate_vehicle_utilization_report(self):
        self.mock_db.fetch_query.return_value = [
            (1, 5), (2, 3)
        ]
        self.service.generate_vehicle_utilization_report()
        self.mock_db.fetch_query.assert_called_once()


    def test_generate_revenue_report(self):
        self.mock_db.fetch_query.return_value = [
            (1, 10000.00), (2, 8000.00)
        ]
        self.service.generate_revenue_report()
        self.mock_db.fetch_query.assert_called_once()


if __name__ == "__main__":
    unittest.main()
