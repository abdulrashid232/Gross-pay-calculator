import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                          (serial_number TEXT PRIMARY KEY,name TEXT, position TEXT, gross_pay REAL)''')
        self.connection.commit()

    def insert_employee(self,  serial_number,name, position, gross_pay):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?)",
                       (serial_number,name, position, gross_pay))
        self.connection.commit()

    def get_all_employees(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT serial_number,name, position, gross_pay FROM employees")
        rows = cursor.fetchall()
        return rows