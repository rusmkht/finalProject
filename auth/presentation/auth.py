import hashlib

from auth.data.auth_file_handler import AuthFileHandler
from search.presentation.movie_search_app import MovieSearchApp

from utils.logger_mixin import LoggerMixin



class Authentication(LoggerMixin):
    API_KEY = "809aa3a061msh922897da2f4ac17p1b81e0jsn7a71aca3649a"

    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.logger = self.setup_logger("Authentication")

    def register(self):
        try:
            loaded_key = self.file_handler.load_key()

            users = self.file_handler.load_users()
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if any(user.startswith(f"{username}:") for user in users):
                self.logger.warning("Username already exists. Please choose another.")
            else:
                users.append(f"{username}:{password_hash}")
                self.file_handler.save_users(users)
                self.logger.info("Registration successful!")

                username_hash = hashlib.sha256(username.encode()).hexdigest()
                self.initialize_movie_search_app(username_hash, loaded_key)

        except FileNotFoundError as e:
            self.logger.error(f"Error: {e}")

    def login(self):
        try:
            loaded_key = self.file_handler.load_key()

            users = self.file_handler.load_users()
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user_data = next((user for user in users if user.startswith(f"{username}:")), None)

            if user_data:
                stored_password_hash = user_data.split(':')[1]

                if hashlib.sha256(password.encode()).hexdigest() == stored_password_hash:
                    self.logger.info("Login successful!")

                    username_hash = hashlib.sha256(username.encode()).hexdigest()
                    print(loaded_key)
                    self.initialize_movie_search_app(username_hash, loaded_key)
                else:
                    self.logger.warning("Login failed. Incorrect password.")
            else:
                self.logger.warning("Login failed. User not found.")

        except FileNotFoundError as e:
            self.logger.error(f"Error: {e}")

    def initialize_movie_search_app(self, username_hash, key):
        api_key = self.API_KEY
        username_hash = f'storage/{username_hash}'
        movie_search_app = MovieSearchApp(api_key, username_hash, key)
        movie_search_app.run()

def main():
    file_handler = AuthFileHandler()
    authentication = Authentication(file_handler)

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            authentication.register()
        elif choice == '2':
            authentication.login()
        elif choice == '3':
            file_handler.logger.info("Exiting the authentication system. Goodbye!")
            break
        else:
            file_handler.logger.warning("Invalid choice. Please choose 1, 2, or 3.")

