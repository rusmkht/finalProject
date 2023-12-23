import os

from cryptography.fernet import Fernet, InvalidToken

from utils.logger_mixin import LoggerMixin


class AuthFileHandler(LoggerMixin):
    def __init__(self, storage_directory='storage/'):
        self.storage_directory = storage_directory
        self.key_filename = os.path.join(self.storage_directory, 'secret.key')
        self.users_filename = os.path.join(self.storage_directory, 'users.txt')

        self.logger = self.setup_logger("FileHandler")
        self.load_key()

    def generate_key(self):
        return Fernet.generate_key()

    def save_key(self, key):
        with open(self.key_filename, 'wb') as key_file:
            key_file.write(key)

    def load_key(self):
        try:
            with open(self.key_filename, 'rb') as key_file:
                self.key = key_file.read()
                return self.key
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(self.key_filename, 'wb') as key_file:
                key_file.write(self.key)

    def encrypt_data(self, data):
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        cipher = Fernet(self.key)
        try:
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            return decrypted_data
        except InvalidToken as e:
            self.logger.error(f"Error decrypting data: {e}")
            self.logger.error(f"Encrypted data: {encrypted_data}")
            raise

    def load_users(self):
        try:
            with open(self.users_filename, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.decrypt_data(encrypted_data)
                return decrypted_data.split('\n')
        except FileNotFoundError:
            return []

    def save_users(self, users):
        users_str = '\n'.join(users)
        encrypted_data = self.encrypt_data(users_str)

        with open(self.users_filename, 'wb') as file:
            file.write(encrypted_data)
