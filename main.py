import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication
from pymongo import MongoClient, errors
from datetime import datetime, timezone

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Load the UI file
            uic.loadUi('main.ui', self)

            # Set fixed size based on loaded UI
            self.setFixedSize(self.size())

            self.connect_bt.clicked.connect(self.connect_server)
            self.save_bt.clicked.connect(self.insert_data)

        except FileNotFoundError:
            print("UI file 'main.ui' not found.")

    def connect_server(self):
        """
        This will connect you to your MongoDB.
        """
        self.mongo_link = self.database_input.text()

        try:
            self.client = MongoClient(self.mongo_link, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
            self.client.admin.command('ping')  # Force connection check
            self.validation_label.setStyleSheet("color: green; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Connected to MongoDB server at {self.mongo_link}")
            print(f"Connected to MongoDB server at {self.mongo_link}")
            self.create_database() 

        except errors.ServerSelectionTimeoutError:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Failed to connect to MongoDB server at {self.mongo_link}")
            print(f"Failed to connect to MongoDB server at {self.mongo_link}")

        except ValueError as e1:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"Invalid MongoDB URI: {e1}")
            print(f"ValueError: {e1}")
            
        except Exception as e:
            self.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
            self.validation_label.setText(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

    def create_database(self):
        '''This will create your databases in your MongoDB.'''
        try:
            self.db = self.client["school_database"]
            self.collection = self.db["students"]  # Create or use the 'students' collection
            print('Database and collection created')
        except AttributeError:
            print('Connection not established. Please connect to the server first.')

    def insert_data(self):
        '''This will insert data into your MongoDB collection.'''
        
        # Ensure the connection and collection are properly set
        if not hasattr(self, 'collection'):
            print('Database or collection not initialized. Please ensure you have connected to the server and created the database.')
            return

        self.school_id = self.school_id_input.text()
        self.first_name = self.first_name_input.text()
        self.last_name = self.last_name_input.text()
        self.birthday = self.birthday_input.text()
        self.gender = self.gender_input.currentText()
        self.school_year = self.school_year_input.currentText()
        self.phone_number = self.phone_input.text()
        self.address = self.address_input.text()
        self.postal = self.postal_input.text()
        self.city = self.city_input.text()
        
        post = {
            "school_id": self.school_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "school_year": self.school_year,
            "phone_number": self.phone_number,
            "address": {
                "address_line": self.address,
                "postal_code": self.postal,
                "city": self.city,
            },
            "date_created": datetime.now(timezone.utc),  # Ensure datetime is timezone aware
        }
        
        try:
            result = self.collection.insert_one(post)
            print(f"Data inserted with record id {result.inserted_id}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyApp()
    main_app.show()
    sys.exit(app.exec())
