from dao.admin_service import AdminService
from dao.customer_service import CustomerService
from dao.vehicle_service import VehicleService
from dao.reservation_service import ReservationService
from entity.admin import Admin
from entity.customer import Customer
from entity.vehicle import Vehicle
from entity.reservation import Reservation
from exceptions import DatabaseConnectionException
from util.db_conn_util import DBConnUtil
from exceptions.admin_not_found_exception import AdminNotFoundException
from exceptions.invalid_input_exception import InvalidInputException
from exceptions.authentication_exception import AuthenticationException
from exceptions.vehicle_not_found_exception import VehicleNotFoundException
from exceptions.reservation_exception import ReservationException
from exceptions.customer_not_found_exception import CustomerNotFoundException

db = DBConnUtil()
admin_service = AdminService(db)
customer_service = CustomerService(db)
vehicle_service = VehicleService(db)
reservation_service = ReservationService(db)

def login_menu():
    while True:
        print("\n===== CarConnect Login Menu =====")
        print("1. Customer Sign Up")
        print("2. Customer Login")
        print("3. Admin Login")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            try:
                first = input("First name: ")
                last = input("Last name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                address = input("Address: ")
                username = input("Username: ")
                password = input("Password: ")
                customer = Customer(None, first, last, email, phone, address, username, password, None)
                customer_service.register_customer(customer)
                print("Customer registered successfully!")
            except InvalidInputException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '2':
            try:
                username = input("Username: ")
                password = input("Password: ")
                customer = customer_service.authenticate_customer(username, password)
                customer_logged_in_menu(customer)
            except (InvalidInputException, AuthenticationException) as e:
                print(f"Login Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '3':
            try:
                username = input("Username: ")
                password = input("Password: ")
                admin = admin_service.authenticate_admin(username, password)
                if admin == 'super admin':
                    super_admin_menu(admin)
                elif admin == 'fleet manager':
                    fleet_admin_menu(admin)
            except (InvalidInputException, AuthenticationException) as e:
                print(f"Admin Login Error: {e}")

        elif choice == '0':
            print("Exiting CarConnect...")
            break

        else:
            print("Invalid option. Try again.")

def customer_logged_in_menu(customer):
    while True:
        print("\n--- Customer Dashboard ---")
        print("1. Update Profile")
        print("2. Check Customer Details")
        print("3. Create Reservation")
        print("4. Get Reservation by ID")
        print("5. Delete Account")
        print("6. Cancel Reservation")  # <-- NEW OPTION
        print("0. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            try:
                customer_id = input("Customer ID: ")
                first_name = input("First Name: ")
                last_name = input("Last Name: ")
                email = input("New Email: ")
                phone = input("New Phone: ")
                address = input("New Address: ")
                username = input("Username: ")
                customer_service.update_customer(customer_id, first_name, last_name, email, phone, address, username)
                print("Customer updated.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")

        elif choice == '2':
            try:
                print(customer_service.get_customer_by_id(input("Customer ID: ")))
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '3':
            try:
                vehicle = vehicle_service.get_available_vehicles()
                customer_id = input("Customer ID: ")
                vehicle_id = input("Vehicle ID: ")
                start_date = input("Start Date (YYYY-MM-DD): ")
                end_date = input("End Date (YYYY-MM-DD): ")

                reservation = Reservation(None, customer_id, vehicle_id, start_date, end_date, total_cost=0,
                                          status="pending")
                reservation_service.create_reservation(reservation)
                print("Reservation created.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '4':
            try:
                reservation_id = input("Reservation ID: ")
                reservation = reservation_service.get_reservation_by_id(reservation_id)
                print(reservation)
            except ReservationException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '5':
            try:
                customer_id = input("Customer ID: ")
                customer_service.delete_customer(customer_id)
                print("Customer deleted.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")

        elif choice == '6':
            try:
                reservation_id = input("Reservation ID to cancel: ")
                reservation_service.cancel_reservation(reservation_id)
                print("Reservation cancelled.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except ReservationException as e:
                print(f"Reservation Error: {e}")

        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def super_admin_menu(admin):
    while True:
        print("\n--- Super Admin Dashboard ---")
        print("1. Register Admin")
        print("2. Get Admin by ID")
        print("3. Get Admin by Username")
        print("4. Update Admin")
        print("5. Delete Admin")
        print("6. Get Customer by ID")
        print("7. Get Customer by Username")
        print("8. Delete Customer")
        print("9. Add Vehicle")
        print("10. Get Vehicle by ID")
        print("11. Get Available Vehicles")
        print("12. Update Vehicle")
        print("13. Delete Vehicle")
        print("14. Get Reservation by ID")
        print("15. Get Reservation by Customer ID")
        print("16. Update Reservation")
        print("17. Cancel Reservation")
        print("18. Generate Reservation History Report")
        print("19. Generate Vehicle Utilization Report")
        print("20. Generate Revenue Report")
        print("0. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            try:
                first = input("First name: ")
                last = input("Last name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                username = input("Username: ")
                password = input("Password: ")
                role = input("Role('super admin', 'fleet manager'): ")

                admin = Admin(None, first, last, email, phone, username, password, role, None)
                admin_service.register_admin(admin)
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except DatabaseConnectionException as e:
                print(f"Database Error: {e}")

        elif choice == '2':
            try:
                admin_id = input("Admin ID: ")
                print(admin_service.get_admin_by_id(admin_id))
            except AdminNotFoundException as e:
                print(f"Admin Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '3':
            try:
                uname = input("Username: ")
                print(admin_service.get_admin_by_username(uname))
            except AdminNotFoundException as e:
                print(f"Admin Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")


        elif choice == '4':
            try:
                admin_id = input("Admin ID: ")
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                email = input("New Email: ")
                phone = input("New Phone: ")
                username = input("New Username: ")
                role = input("Role('super admin', 'fleet manager'): ")
                admin_service.update_admin(admin_id, first_name, last_name, email, phone, username, role)
                print("Admin updated.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except DatabaseConnectionException as e:
                print(f"Registration Failed: {e}")

        elif choice == '5':
            try:
                admin_id = input("Admin ID to delete: ")
                admin_service.delete_admin(admin_id)
            except AdminNotFoundException as e:
                print(f"Admin Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '6':
            try:
                cid = input("Customer ID: ")
                print(customer_service.get_customer_by_id(cid))
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '7':
            try:
                uname = input("Username: ")
                print(customer_service.get_customer_by_username(uname))
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '8':
            try:
                cid = input("Customer ID to delete: ")
                customer_service.delete_customer(cid)
                print("Customer deleted.")
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        if choice == '9':
            try:
                model = input("Model: ")
                make = input("Make: ")
                year = input("Year: ")
                color = input("Color: ")
                reg_no = input("Registration Number: ")
                availability = input("Availability (1/0): ")
                daily_rate = input("Daily Rate: ")
                vehicle = Vehicle(None, model, make, year, color, reg_no, availability, daily_rate)
                vehicle_service.add_vehicle(vehicle)
                print("Vehicle added.")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except DatabaseConnectionException as e:
                print(f"Registration Failed: {e}")

        elif choice == '10':
            try:
                vid = input("Vehicle ID: ")
                print(vehicle_service.get_vehicle_by_id(vid))
            except VehicleNotFoundException as e:
                print(f"Vehicle Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '11':
            try:
                print(vehicle_service.get_available_vehicles())
            except VehicleNotFoundException as e:
                print(f"Error: {e}")

        elif choice == '12':
            try:
                vid = input("Vehicle ID to update: ")
                rate = input("New daily rate: ")
                availability = input("Availability (1 or 0): ")
                vehicle_service.update_vehicle(vid, rate, availability)
            except VehicleNotFoundException as e:
                print(f"Vehicle Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '13':
            try:
                vid = input("Vehicle ID to delete: ")
                vehicle_service.remove_vehicle(vid)
            except VehicleNotFoundException as e:
                print(f"Vehicle Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '14':
            try:
                rid = input("Reservation ID: ")
                print(reservation_service.get_reservation_by_id(rid))
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '15':
            try:
                cid = input("Customer ID: ")
                print(reservation_service.get_reservations_by_customer_id(cid))
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '16':
            try:
                rid = input("Reservation ID: ")
                status = input("New status (pending/confirmed/completed): ")
                reservation_service.update_reservation(rid, status)
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '17':
            try:
                rid = input("Reservation ID to cancel: ")
                reservation_service.cancel_reservation(rid)
                print("Reservation cancelled.")
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '18':
            try:
                reservation_service.generate_reservation_history_report()
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '19':
            try:
                reservation_service.generate_vehicle_utilization_report()
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '20':
            try:
                reservation_service.generate_revenue_report()
            except Exception as e:
                print(f"Unexpected error: {e}")

        elif choice == '0':
            break
        else:
            print("Invalid choice.")

def fleet_admin_menu(admin):
    while True:
        print("\n--- Fleet Admin Dashboard ---")
        print("1. Get Admin by ID")
        print("2. Get Admin by Username")
        print("3. Get Customer by ID")
        print("4. Get Customer by Username")
        print("5. Delete Customer")
        print("6. List Available Vehicles")
        print("7. Update Vehicle")
        print("8. Show Confirmed Reservations")
        print("9. Show Pending Reservations")
        print("10. Update Reservation Status")
        print("11. Get Reservation by Customer ID")
        print("0. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            try:
                print(admin_service.get_admin_by_id(input("Admin ID: ")))
            except AdminNotFoundException as e:
                print(f"Admin Error: {e}")

        elif choice == '2':
            try:
                print(admin_service.get_admin_by_username(input("Username: ")))
            except AdminNotFoundException as e:
                print(f"Admin Error: {e}")

        elif choice == '3':
            try:
                print(customer_service.get_customer_by_id(input("Customer ID: ")))
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '4':
            try:
                print(customer_service.get_customer_by_username(input("Username: ")))
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '5':
            try:
                customer_service.delete_customer(input("Customer ID: "))
                print("Customer deleted successfully.")
            except CustomerNotFoundException as e:
                print(f"Customer Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '6':
            try:
                available_vehicles = vehicle_service.get_available_vehicles()
            except VehicleNotFoundException as e:
                print(f"Vehicle Error: {e}")

        elif choice == '7':
            try:
                vehicle_id = input("Vehicle ID: ")
                daily_rate = input("New Daily Rate: ")
                availability = input("Availability (1/0): ")
                vehicle_service.update_vehicle(vehicle_id, daily_rate, availability)
                print("Vehicle updated successfully.")
            except VehicleNotFoundException as e:
                print(f"Vehicle Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '8':
            try:
                confirmed = reservation_service.get_confirmed_reservation()
            except ReservationException as e:
                print(f"ReservationError:{e}")

        elif choice == '9':
            try:
                pending = reservation_service.get_pending_reservation()
            except ReservationException as e:
                print(f"Reservation Error: {e}")

        elif choice == '10':
            try:
                reservation_id = input("Reservation ID: ")
                status = input("New Status (pending/confirmed/completed): ")
                reservation_service.update_reservation(reservation_id, status)
                print("Reservation status updated.")
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '11':
            try:
                customer_id = input("Customer ID: ")
                reservations = reservation_service.get_reservations_by_customer_id(customer_id)
            except ReservationException as e:
                print(f"Reservation Error: {e}")
            except InvalidInputException as e:
                print(f"Input Error: {e}")

        elif choice == '0':
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    login_menu()
