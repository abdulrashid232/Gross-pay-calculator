from database import Database

class Employee:
    def __init__(self, name, serial_number, position):
        self.name = name
        self.serial_number = serial_number
        self.position = position

def calculate_gross_pay(hours, rate_per_hour, is_management):
    # Calculate gross pay based on hours worked and rate per hour
    if 30 <= hours <= 40:
        rate_per_hour += 50  # Increase rate per hour by 50 if hours are between 30 and 40
    if is_management:
        rate_per_hour += 50  # Increase rate per hour by 50 if the employee is in a management position
    gross_pay = hours * rate_per_hour
    return gross_pay

# Create an instance of the Database class
database = Database('employee_data.db')

# Connect to the database
connection = database.connect()

# Create the table if it doesn't exist
database.create_table()

num_employees = int(input("number of employee"))
rate_per_hour = 2.75  # Constant rate per hour

# Get employee details from user input and store in the database
for i in range(num_employees):
    name = input(f"\nEnter employee {i+1}'s name: ").strip()
    while not name:
        print("Name cannot be blank. Please enter the employee's name.")
        name = input(f"Enter employee {i+1}'s name: ")

    while True:
        serial_number = input(f"Enter employee {i+1}'s serial number: ").replace(" ","")
        if serial_number:
            cursor = connection.cursor()
            cursor.execute("SELECT serial_number FROM employees WHERE serial_number=?", (serial_number,))
            existing_serial_number = cursor.fetchone()
            if existing_serial_number:
                print("Serial number already exists. Please enter a unique serial number.")
            else:
                break
        else:
            print("Serial number cannot be blank. Please enter a unique serial number.")

    position = input(f"Enter employee {i+1}'s position: ")

    # Calculate gross pay for the employee
    while True:
        hours_input = input(f"Enter hours worked by {name}: ")
        if hours_input:
            try:
                hours = float(hours_input)
                if hours < 0:
                    raise ValueError("Hours cannot be negative.")
                break
            except ValueError:
                print("Invalid input. Please enter a valid number for hours.")
        else:
            print("Input cannot be blank. Please enter the number of hours.")

    is_management = position.lower() == "manager"
    gross_pay = calculate_gross_pay(hours, rate_per_hour, is_management)

    # Store employee data in the database
    database.insert_employee( serial_number,name, position, gross_pay)

# Retrieve employee data from the database
rows = database.get_all_employees()
print("")

# Display employee information
print("Employee Information:")
for i, row in enumerate(rows):
    serial_number, name,  position, gross_pay = row
    print(f"\nEmployee {i+1}:")
    print(f" Serial Number: {serial_number},Name: {name}, Position: {position}, Gross Pay: {gross_pay} cedis")

# Disconnect from the database
database.disconnect()
