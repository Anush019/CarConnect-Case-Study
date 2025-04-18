from entity.reservation import Reservation
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.reservation_exception import ReservationException
from datetime import datetime
from tabulate import tabulate


class ReservationService():
    def __init__(self, db):
        self.db = db

    def get_reservation_by_id(self, reservation_id):
        if not reservation_id.isdigit():
            raise InvalidInputException("Reservation ID must be an integer.")

        query = "SELECT * FROM Reservation WHERE ReservationID = %s"
        result = self.db.fetch_query(query, (reservation_id,))
        if not result:
            raise ReservationException(f"No reservation found with ID: {reservation_id}")
        headers = ["ReservationID", "CustomerID", "VehicleID", "StartDate", "EndDate", "TotalCost", "Status"]
        print(tabulate(result, headers=headers, tablefmt="fancy_grid"))

    def get_reservations_by_customer_id(self, customer_id):
        if not customer_id.isdigit():
            raise InvalidInputException("Customer ID must be an integer.")

        query = "SELECT * FROM Reservation WHERE CustomerID = %s"
        result = self.db.fetch_query(query, (customer_id,))

        if not result:
            raise ReservationException(f"No reservations found for customer ID: {customer_id}")

        headers = ["ReservationID", "CustomerID", "VehicleID", "StartDate", "EndDate", "TotalCost", "Status"]
        print(tabulate(result, headers=headers, tablefmt="fancy_grid"))

    def create_reservation(self, reservation):
        if not reservation.customer_id.isdigit() or not reservation.vehicle_id.isdigit():
            raise InvalidInputException("Customer ID and Vehicle ID must be integers.")


        query = "SELECT Availability, DailyRate FROM Vehicle WHERE VehicleID = %s"
        result = self.db.fetch_one(query, (reservation.vehicle_id,))
        if not result:
            raise ReservationException("Vehicle does not exist.")
        if result[0] != 1:
            raise ReservationException("Vehicle is not available for reservation.")

        daily_rate = result[1]


        start_date = datetime.strptime(reservation.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(reservation.end_date, "%Y-%m-%d")
        number_of_days = (end_date - start_date).days
        if number_of_days <= 0:
            raise InvalidInputException("End date must be after start date.")

        total_cost = number_of_days * daily_rate


        insert_query = """
            INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(insert_query, (
            reservation.customer_id, reservation.vehicle_id,
            reservation.start_date, reservation.end_date,
            total_cost, reservation.status
        ))

        self.db.conn.commit()


        reservation_id = self.db.cursor.lastrowid

        print(f"Reservation created successfully with ID: {reservation_id}")
        print(f"Total cost calculated: ₹{total_cost:.2f}")

    def update_reservation(self, reservation_id, status):
        if not reservation_id.isdigit():
            raise InvalidInputException("Reservation ID must be an integer.")

        query = "UPDATE Reservation SET Status = %s WHERE ReservationID = %s"
        rowcount = self.db.execute_query(query, (status, reservation_id))

        if rowcount == 0:
            raise ReservationException(f"No reservation found with ID: {reservation_id}")

    def cancel_reservation(self, reservation_id):
        if not reservation_id.isdigit():
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

        if not results:
            raise ReservationException("No reservations found.")

        headers = ["Reservation ID", "Customer ID", "Vehicle ID", "Start Date", "End Date", "Status"]
        print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

    def generate_vehicle_utilization_report(self):
        query = """
            SELECT VehicleID, COUNT(*) AS TotalReservations
            FROM Reservation
            GROUP BY VehicleID
            ORDER BY TotalReservations DESC
        """
        results = self.db.fetch_query(query)
        print("\n--- Vehicle Utilization Report ---")

        if not results:
            raise ReservationException("No reservation data available.")

        headers = ["Vehicle ID", "Total Reservations"]
        print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

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

        if not results:
            raise ReservationException("No completed reservations found.")


        formatted_results = [(row[0], f"₹{row[1]:.2f}") for row in results]
        headers = ["Vehicle ID", "Revenue"]

        print(tabulate(formatted_results, headers=headers, tablefmt="fancy_grid"))

    def get_pending_reservation(self):
        query = "SELECT * from Reservation WHERE Status = 'Pending'"
        rows = self.db.fetch_query(query)
        if not rows:
            raise ReservationException("No Pending reservations")

        headers = ["ReservationID", "CustomerID", "VehicleID", "StartDate", "EndDate", "TotalCost", "Status"]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

    def get_confirmed_reservation(self):
        query = "SELECT * from Reservation WHERE Status = 'Confirmed'"
        rows = self.db.fetch_query(query)
        if not rows:
            raise ReservationException("No Confirmed reservations")

        headers = ["ReservationID", "CustomerID", "VehicleID", "StartDate", "EndDate", "TotalCost", "Status"]
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
