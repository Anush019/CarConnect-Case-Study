from CarConnect.entity.vehicle import Vehicle
from CarConnect.exceptions.vehicle_not_found_exception import VehicleNotFoundException
from CarConnect.exceptions.invalid_input_exception import InvalidInputException
from CarConnect.exceptions.database_connection_exception import DatabaseConnectionException

class VehicleService(Vehicle):
    def __init__(self, db):
        self.db = db

    def get_vehicle_by_id(self, vehicle_id):
        if not isinstance(vehicle_id, int):
            raise InvalidInputException("Vehicle ID must be an integer.")
        try:
            query = "SELECT * FROM Vehicle WHERE VehicleID = %s"
            row = self.db.fetch_query(query, (vehicle_id,))
            if not row:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
            print("The vehicle is: ",row)
        except Exception as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def get_available_vehicles(self):
        try:
            query = "SELECT * FROM Vehicle WHERE Availability = 1"
            rows = self.db.fetch_query(query)
            if not rows:
                raise VehicleNotFoundException("No available vehicles found.")
            return rows
        except Exception as e:
            raise DatabaseConnectionException(f"Database error: {str(e)}")

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise InvalidInputException("Invalid vehicle object.")
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
        if not isinstance(vehicle_id, int):
            raise InvalidInputException("Vehicle ID must be an integer.")
        try:
            query = """
                UPDATE Vehicle SET DailyRate = %s, Availability = %s WHERE VehicleID = %s
            """
            result = self.db.execute_query(query, (daily_rate, availability, vehicle_id))
            if result == 0:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to update vehicle: {str(e)}")

    def remove_vehicle(self, vehicle_id):
        if not isinstance(vehicle_id, int):
            raise InvalidInputException("Vehicle ID must be an integer.")
        try:
            query = "DELETE FROM Vehicle WHERE VehicleID = %s"
            result = self.db.execute_query(query, (vehicle_id,))
            if result == 0:
                raise VehicleNotFoundException(f"No vehicle found with ID: {vehicle_id}")
        except Exception as e:
            raise DatabaseConnectionException(f"Failed to delete vehicle: {str(e)}")
