from CarConnect.entity.reservation import Reservation
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.reservation_exception import ReservationException

class ReservationService(Reservation):
    def __init__(self, db):
        self.db = db

    def get_reservation_by_id(self, reservation_id):
        if not isinstance(reservation_id, int):
            raise InvalidInputException("Reservation ID must be an integer.")

        query = "SELECT * FROM Reservation WHERE ReservationID = %s"
        result = self.db.fetch_query(query, (reservation_id,))

        if not result:
            raise ReservationException(f"No reservation found with ID: {reservation_id}")

        return Reservation(*result[0])

    def get_reservations_by_customer_id(self, customer_id):
        if not isinstance(customer_id, int):
            raise InvalidInputException("Customer ID must be an integer.")

        query = "SELECT * FROM Reservation WHERE CustomerID = %s"
        result = self.db.fetch_query(query, (customer_id,))

        if not result:
            raise ReservationException(f"No reservations found for customer ID: {customer_id}")

        for row in result:
            reservation = Reservation(*row)
            print(f"Reservation ID: {reservation.reservation_id}")
            print(f"Vehicle ID   : {reservation.vehicle_id}")
            print(f"Start Date   : {reservation.start_date}")
            print(f"End Date     : {reservation.end_date}")
            print(f"Total Cost   : {reservation.total_cost}")
            print(f"Status       : {reservation.status}")

    def create_reservation(self, reservation):
        if not isinstance(reservation, Reservation):
            raise InvalidInputException("Invalid reservation object.")

        query = """
            INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (
            reservation.customer_id, reservation.vehicle_id, reservation.start_date,
            reservation.end_date, reservation.total_cost, reservation.status
        ))

    def update_reservation(self, reservation_id, status):
        if not isinstance(reservation_id, int):
            raise InvalidInputException("Reservation ID must be an integer.")

        query = "UPDATE Reservation SET Status = %s WHERE ReservationID = %s"
        rowcount = self.db.execute_query(query, (status, reservation_id))

        if rowcount == 0:
            raise ReservationException(f"No reservation found with ID: {reservation_id}")

    def cancel_reservation(self, reservation_id):
        if not isinstance(reservation_id, int):
            raise InvalidInputException("Reservation ID must be an integer.")

        query = "DELETE FROM Reservation WHERE ReservationID = %s"
        rowcount = self.db.execute_query(query, (reservation_id,))

        if rowcount == 0:
            raise ReservationException(f"No reservation found with ID: {reservation_id}")

    def generate_reservation_history_report(self):
        query = """
            SELECT ReservationID, CustomerID, VehicleID, StartDate, EndDate, Status
            FROM Reservation
            ORDER BY StartDate DESC
        """
        results = self.db.fetch_query(query)
        print("\n--- Reservation History Report ---")
        for row in results:
            print(row)

    def generate_vehicle_utilization_report(self):
        query = """
            SELECT VehicleID, COUNT(*) AS TotalReservations
            FROM Reservation
            GROUP BY VehicleID
            ORDER BY TotalReservations DESC
        """
        results = self.db.fetch_query(query)
        print("\n--- Vehicle Utilization Report ---")
        for row in results:
            print(f"Vehicle ID: {row[0]}, Reservations: {row[1]}")

    def generate_revenue_report(self):
        query = """
            SELECT VehicleID, SUM(TotalCost) AS Revenue
            FROM Reservation
            WHERE Status = 'Completed'
            GROUP BY VehicleID
            ORDER BY Revenue DESC
        """
        results = self.db.fetch_query(query)
        print("\n--- Revenue Report ---")
        for row in results:
            print(f"Vehicle ID: {row[0]}, Revenue: ₹{row[1]:.2f}")


