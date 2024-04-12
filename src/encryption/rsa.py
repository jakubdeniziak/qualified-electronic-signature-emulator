from abc import ABC, abstractmethod
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from encryption.aes import CryptographyAes
from gui.window import input_password
from src.utils.file_operations import save_to_file, load_from_file, save_multiple_to_file


class Rsa(ABC):
    def __init__(self):
        self._KEY_SIZE = 4096
        self._PUBLIC_EXPONENT = 65537
        self._private_key = None
        self._public_key = None
        self._key_id = None

    @abstractmethod
    def generate_keys(self):
        pass

    @abstractmethod
    def _save_public_key(self):
        pass

    @abstractmethod
    def _save_private_key(self):
        pass

    @staticmethod
    @abstractmethod
    def load_public_key(file_path):
        pass

    @staticmethod
    @abstractmethod
    def load_private_key(file_path):
        pass


class CryptographyRsa(Rsa):
    def generate_keys(self):
        self._private_key = rsa.generate_private_key(
            public_exponent=self._PUBLIC_EXPONENT,
            key_size=self._KEY_SIZE
        )
        self._public_key = self._private_key.public_key()
        self._key_id = hash(datetime.now())
        self._save_public_key()
        self._save_private_key()

    def _save_public_key(self):
        file_name = f'public_key-{self._key_id}.pem'
        save_to_file(
            file_name=file_name,
            content=self._public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    def _save_private_key(self):
        aes = CryptographyAes()
        passphrase = input_password().encode('utf-8')
        salt, key = aes.derive_key_from_passphrase(passphrase)
        initialization_vector, encrypted_private_key = aes.encrypt(key, self.__get_private_key_bytes())

        file_name = f'private_key-{self._key_id}.pem'
        save_multiple_to_file(
            file_name=file_name,
            content=(
                salt,
                initialization_vector,
                encrypted_private_key
            )
        )

    def __get_private_key_bytes(self):
        private_key_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_key_bytes

    @staticmethod
    def load_public_key(file_path):
        public_key = serialization.load_pem_public_key(
            load_from_file(file_path),
            backend=default_backend()
        )
        return public_key

    @staticmethod
    def load_private_key(file_path):
        private_key = serialization.load_pem_private_key(
            load_from_file(file_path),
            password=None,
            backend=default_backend()
        )
        return private_key
