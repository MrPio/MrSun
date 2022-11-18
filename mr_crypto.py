import os
import pickle

import userpaths
from cryptography.fernet import Fernet


class MrCrypto:
    def __init__(self, key_path=userpaths.get_desktop()+"\\ALTRO\\my.key"):
        self.key_path = key_path
        if not os.path.exists(key_path):
            MrCrypto.generate_key(key_path)
        with open(key_path, 'rb') as f:
            self.key = pickle.load(f)

    def encrypt(self, message: str) -> str:
        return Fernet(self.key).encrypt(message.encode()).decode()

    def decrypt(self, token: str) -> str:
        return Fernet(self.key).decrypt(token.encode()).decode()

    @staticmethod
    def generate_key(where: str) -> str:
        key = Fernet.generate_key()
        with open(f'{where}\\my.key', 'wb') as f:
            pickle.dump(key, f, protocol=pickle.HIGHEST_PROTOCOL)
        return f'{where}\\my.key'