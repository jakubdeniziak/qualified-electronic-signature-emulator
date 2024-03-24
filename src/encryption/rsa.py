from abc import ABC, abstractmethod
from datetime import datetime

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class Rsa(ABC):
    def __init__(self):
        self._KEY_SIZE = 4096
        self._PUBLIC_EXPONENT = 65537
        self._private_key = None
        self._public_key = None

    @abstractmethod
    def generate_keys(self):
        pass

    def _save_public_key(self):
        now_hash = hash(datetime.now())
        file_name = f'public_key-{now_hash}.pem'

        with open(file_name, 'wb') as key_file:
            key_file.write(
                self._public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )


class CryptographyRsa(Rsa):
    def generate_keys(self):
        self._private_key = rsa.generate_private_key(
            public_exponent=self._PUBLIC_EXPONENT,
            key_size=self._KEY_SIZE
        )
        self._public_key = self._private_key.public_key()
        self._save_public_key()
