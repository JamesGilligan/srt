#database

import mysql.connector
from PyQt6.QtWidgets import QMessageBox

class DatabaseManager:
    def init(self, host, user, password, database):

        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )


    def close_connection(self):
        if self.db_connection.is_connected():
            self.db_connection.close()

class UserManager:
    def init(self, db_manager):
        self.db_manager = db_manager

    def email_exists(self, email):
        cursor = self.db_manager.db_connection.cursor()

        query = "SELECT * FROM admin WHERE email = %s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        return user is not None

    def username_exists(self, username):
        cursor = self.db_manager.db_connection.cursor()
        query = "SELECT * FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        return user is not None

    def login(self, username, password):
        cursor = self.db_manager.db_connection.cursor()

        # Execute SELECT query to check login admin
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        cursor.close()

        if user:
            QMessageBox.information(None, 'Login Successful', f'Welcome, {username}')
            return True
        else:
            QMessageBox.warning(None, 'Login Failed', 'Invalid username, password.')
            return False 