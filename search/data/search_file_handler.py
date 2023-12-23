import json
import os

from cryptography.fernet import Fernet


class SearchFileHandler:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def create_directory(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    def encrypt(self, data):
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(data.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher = Fernet(self.key)
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        return decrypted_data

    def read_json(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                encrypted_data = file.read()
                if encrypted_data:
                    decrypted_data = self.decrypt(encrypted_data)
                    return json.loads(decrypted_data) if decrypted_data else []
                else:
                    return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON from {file_path}: {e}")
            return []

    def write_json(self, file_path, data):
        existing_data = self.read_json(file_path)
        existing_data.append(data)

        encrypted_data = self.encrypt(json.dumps(existing_data))
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
