#database

import mysql.connector
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, host, user, password, database):
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
    def __init__(self, db_manager):
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

        if user:
            # Reset login attempts on successful login
            self.reset_login_attempts(username)
            QMessageBox.information(None, 'Login Successful', f'Welcome, {username}')
            return True
        else:
            # Increment login attempts and set indefinite lockout
            self.handle_login_attempts(username)
            return False

    def handle_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Retrieve current login attempts count and lockout status
        query = "SELECT login_attempts, locked_out_until FROM admin WHERE username = %s"
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()

        if user_info:
            login_attempts, locked_out_until = user_info

            # Increment login attempts
            login_attempts += 1

            # Set indefinite lockout
            locked_out_until = datetime.max

            # Update login attempts and lockout status in the database
            update_query = "UPDATE admin SET login_attempts = %s, locked_out_until = %s WHERE username = %s"
            cursor.execute(update_query, (login_attempts, locked_out_until, username))

            # Display lockout message
            QMessageBox.warning(None, 'Account Locked', 'Too many unsuccessful login attempts.')

        cursor.close()

    def reset_login_attempts(self, username):
        cursor = self.db_manager.db_connection.cursor()

        # Reset login attempts and lockout status on successful login
        query = "UPDATE admin SET login_attempts = 0, locked_out_until = NULL WHERE username = %s"
        cursor.execute(query, (username,))

        cursor.close()
