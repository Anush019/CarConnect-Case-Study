from entity.vehicle import Vehicle
from exceptions.vehicle_not_found_exception import VehicleNotFoundException
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.database_connection_exception import DatabaseConnectionException
import re

class VehicleService():
    def __init__(self, db):
        self.db = db

    def get_vehicle_by_id(self, vehicle_id):
        try:
            query = "SELECT * FROM Vehicle WHERE VehicleID = %s"
            row = self.db.fetch_query(query, (vehicle_id,))
            if not row:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
            print("The vehicle is: ",row)
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def get_available_vehicles(self):
        try:
            query = "SELECT * FROM Vehicle WHERE Availability = 1"
            rows = self.db.fetch_query(query)
            return rows
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def add_vehicle(self, vehicle):
        pattern = r'^[A-Za-z]{2}\s?[0-9]{2}\s?[A-Za-z]{2}\s?[0-9]{4}$'
        def is_valid_format(text):
            return bool(re.match(pattern, text))
        if not is_valid_format(vehicle.registration_number):
            raise InvalidInputException("Enter valid registration number")

        if not vehicle.year.isdigit() or len(vehicle.year) != 4:
            raise InvalidInputException("Year must be a valid integer.")
        try:
            query = """
                INSERT INTO Vehicle (Model, Make, Year, Color, RegistrationNumber, Availability, DailyRate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                vehicle.model, vehicle.make, vehicle.year, vehicle.color,
                vehicle.registration_number, vehicle.availability, vehicle.daily_rate
            )
            self.db.execute_query(query, values)
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to add vehicle: {str(e)}")

    def update_vehicle(self, vehicle_id, daily_rate, availability):
        if not vehicle_id.isdigit():
            raise InvalidInputException("Vehicle ID must be an integer.")
        try:
            query = """
                UPDATE Vehicle SET DailyRate = %s, Availability = %s WHERE VehicleID = %s
            """
            result = self.db.execute_query(query, (daily_rate, availability, vehicle_id))
            if result == 0:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Failed to update vehicle: {str(e)}")

    def remove_vehicle(self, vehicle_id):
        if not vehicle_id.isdigit():
            raise InvalidInputException("Vehicle ID must be an integer.")
        try:
            query = "DELETE FROM Vehicle WHERE VehicleID = %s"
            result = self.db.execute_query(query, (vehicle_id,))
            if result == 0:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
        except DatabaseConnectionException as e:
            raise DatabaseConnectionException(f"Failed to delete vehicle: {str(e)}")
