from CarConnect.dao.admin_service import AdminService
from CarConnect.dao.customer_service import CustomerService
from CarConnect.dao.vehicle_service import VehicleService
from CarConnect.dao.reservation_service import ReservationService
from CarConnect.entity.admin import Admin
from CarConnect.entity.customer import Customer
from CarConnect.entity.vehicle import Vehicle
from CarConnect.entity.reservation import Reservation
from CarConnect.util.db_conn_util import DBConnUtil

db = DBConnUtil()
admin_service = AdminService(db)
customer_service = CustomerService(db)
vehicle_service = VehicleService(db)
reservation_service = ReservationService(db)

def admin_menu():
    print("\n--- Admin Menu ---")
    print("1. Register Admin")
    print("2. Get Admin by ID")
    print("3. Get Admin by Username")
    print("4. Update Admin")
    print("5. Delete Admin")

    choice = input("Enter choice: ")

    if choice == '1':
        first = input("First name: ")
        last = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        username = input("Username: ")
        password = input("Password: ")
        role = input("Role('super admin', 'fleet manager'): ")

        admin = Admin(None, first, last, email, phone, username, password, role, None)
        admin_service.register_admin(admin)
        print("Admin registered successfully.")

    elif choice == '2':
        admin_id = int(input("Admin ID: "))
        admin = admin_service.get_admin_by_id(admin_id)
        print(admin)

    elif choice == '3':
        username = input("Enter Username: ")
        admin = admin_service.get_admin_by_username(username)
        print(admin)

    elif choice == '4':
        admin_id = int(input("Admin ID: "))
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("New Email: ")
        phone = input("New Phone: ")
        username = input("New Username: ")
        role = input("Role('super admin', 'fleet manager'): ")
        admin_service.update_admin(admin_id,first_name,last_name ,email, phone,username, role)
        print("Admin updated.")

    elif choice == '5':
        admin_id = int(input("Admin ID: "))
        admin_service.delete_admin(admin_id)
        print("Admin deleted.")

def customer_menu():
    print("\n--- Customer Menu ---")
    print("1. Register Customer")
    print("2. Get Customer by ID")
    print("3. Get Customer by Username")
    print("4. Update Customer")
    print("5. Delete Customer")
    print("6. Authenticate Customer")

    choice = input("Enter choice: ")

    if choice == '1':
        first = input("First name: ")
        last = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        address = input("Address: ")
        username = input("Username: ")
        password = input("Password: ")

        customer = Customer(None, first, last, email, phone, address, username, password, None)
        customer_service.register_customer(customer)
        print("Customer registered.")

    elif choice == '2':
        customer_id = int(input("Customer ID: "))
        customer = customer_service.get_customer_by_id(customer_id)
        print(customer)

    elif choice == '3':
        username = input("Enter Username: ")
        customer = customer_service.get_customer_by_username(username)
        print(customer)

    elif choice == '4':
        customer_id = int(input("Customer ID: "))
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("New Email: ")
        phone = input("New Phone: ")
        address = input("New Address: ")
        username = input("Username: ")
        customer_service.update_customer(customer_id,first_name,last_name, email, phone, address,username)
        print("Customer updated.")

    elif choice == '5':
        customer_id = int(input("Customer ID: "))
        customer_service.delete_customer(customer_id)
        print("Customer deleted.")

    elif choice == '6':
        username = input("Username: ")
        password = input("Password: ")
        customer = customer_service.authenticate_customer(username, password)
        print(customer)
        print("Authentication successful!")

def vehicle_menu():
    print("\n--- Vehicle Menu ---")
    print("1. Add Vehicle")
    print("2. Get Vehicle by ID")
    print("3. List Available Vehicles")
    print("4. Update Vehicle")
    print("5. Remove Vehicle")

    choice = input("Enter choice: ")

    if choice == '1':
        model = input("Model: ")
        make = input("Make: ")
        year = int(input("Year: "))
        color = input("Color: ")
        reg_no = input("Registration Number: ")
        availability = int(input("Availability (1/0): "))
        daily_rate = float(input("Daily Rate: "))

        vehicle = Vehicle(None, model, make, year, color, reg_no, availability, daily_rate)
        vehicle_service.add_vehicle(vehicle)
        print("Vehicle added.")

    elif choice == '2':
        vehicle_id = int(input("Vehicle ID: "))
        vehicle = vehicle_service.get_vehicle_by_id(vehicle_id)
        print(vehicle)

    elif choice == '3':
        vehicles = vehicle_service.get_available_vehicles()
        for v in vehicles:
            print(v)

    elif choice == '4':
        vehicle_id = int(input("Vehicle ID: "))
        rate = float(input("New Daily Rate: "))
        availability = int(input("Availability (1/0): "))
        vehicle_service.update_vehicle(vehicle_id, rate, availability)
        print("Vehicle updated.")

    elif choice == '5':
        vehicle_id = int(input("Vehicle ID: "))
        vehicle_service.remove_vehicle(vehicle_id)
        print("Vehicle removed.")

def reservation_menu():
    print("\n--- Reservation Menu ---")
    print("1. Create Reservation")
    print("2. Get Reservation by ID")
    print("3. Get Reservations by Customer ID")
    print("4. Update Reservation Status")
    print("5. Cancel Reservation")
    print("6. Reservation History Report")
    print("7. Generate Vehicle Report")
    print("8. Generate Revenue Report")

    choice = input("Enter choice: ")

    if choice == '1':
        customer_id = int(input("Customer ID: "))
        vehicle_id = int(input("Vehicle ID: "))
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        total_cost = float(input("Total Cost: "))
        status = input("Status: ")

        reservation = Reservation(None, customer_id, vehicle_id, start_date, end_date, total_cost, status)
        reservation_service.create_reservation(reservation)
        print("Reservation created.")

    elif choice == '2':
        reservation_id = int(input("Reservation ID: "))
        reservation = reservation_service.get_reservation_by_id(reservation_id)
        print(reservation)

    elif choice == '3':
        customer_id = int(input("Customer ID: "))
        reservations = reservation_service.get_reservations_by_customer_id(customer_id)

    elif choice == '4':
        reservation_id = int(input("Reservation ID: "))
        status = input("New Status: ")
        reservation_service.update_reservation(reservation_id, status)
        print("Reservation updated.")

    elif choice == '5':
        reservation_id = int(input("Reservation ID: "))
        reservation_service.cancel_reservation(reservation_id)
        print("Reservation canceled.")

    elif choice == '6':
        reservation_service.generate_reservation_history_report()

    elif choice == '7':
        reservation_service.generate_vehicle_utilization_report()

    elif choice == '8':
        reservation_service.generate_revenue_report()

def main():
    while True:
        print("\n===== CarConnect Main Menu =====")
        print("1. Admin Services")
        print("2. Customer Services")
        print("3. Vehicle Services")
        print("4. Reservation Services")
        print("0. Exit")

        option = input("Select option: ")

        if option == '1':
            admin_menu()
        elif option == '2':
            customer_menu()
        elif option == '3':
            vehicle_menu()
        elif option == '4':
            reservation_menu()
        elif option == '0':
            print("Exiting CarConnect...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
