from pymongo import MongoClient, errors
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication
from pymongo import MongoClient, errors


class Pymongo_databases:
    def __init__(self, ui):
        self.ui = ui  # Store the UI instance

    def connect_server(self):
        """
        Connects to MongoDB and updates the UI with the connection status.
        """
        try:
            self.mongo_link = self.ui.database_input.text()  # Access input field from MyApp
            self.client = MongoClient(self.mongo_link)
            self.client.admin.command('ping')  # Force connection check
            
            # Ensure validation_label exists before using it
            if hasattr(self.ui, 'validation_label'):
                self.ui.validation_label.setStyleSheet("color: green; font: 14pt 'MS Shell Dlg 2';")
                self.ui.validation_label.setText(f"Connected to MongoDB server at {self.mongo_link}")
            else:
                print("Error: validation_label is missing in the UI.")
            
            print(f"Connected to MongoDB server at {self.mongo_link}")

        except errors.ServerSelectionTimeoutError:
            if hasattr(self.ui, 'validation_label'):
                self.ui.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
                self.ui.validation_label.setText(f"Failed to connect to MongoDB server at {self.mongo_link}")
            print(f"Failed to connect to MongoDB server at {self.mongo_link}")

        except ValueError as e1:
            if hasattr(self.ui, 'validation_label'):
                self.ui.validation_label.setStyleSheet("color: red; font: 14pt 'MS Shell Dlg 2';")
                self.ui.validation_label.setText(f"Invalid MongoDB URI: {e1}")
            print(f"ValueError: {e1}")
            
