from abc import ABC, abstractmethod
from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from encryption.aes import CryptographyAes
from gui.window import input_password
from utils.file_operations import save_to_file, load_from_file, serialize, deserialize


class Rsa(ABC):
    def __init__(self):
        self._KEY_SIZE = 4096
        self._PUBLIC_EXPONENT = 65537
        self._private_key = None
        self._public_key = None
        self._key_id = None
        self._directory_path = None

    @abstractmethod
    def generate_keys(self, directory_path):
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
    def generate_keys(self, directory_path):
        self._private_key = rsa.generate_private_key(
            public_exponent=self._PUBLIC_EXPONENT,
            key_size=self._KEY_SIZE
        )
        self._public_key = self._private_key.public_key()
        self._key_id = hash(datetime.now())
        self._directory_path = directory_path
        self._save_public_key()
        self._save_private_key()

    def _save_public_key(self):
        file_name = f'public_key-{self._key_id}.pem'
        save_to_file(
            file_name=file_name,
            content=self._public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ),
            directory_path=self._directory_path
        )

    def _save_private_key(self):
        aes = CryptographyAes()
        passphrase = input_password().encode('utf-8')
        salt, key = aes.derive_key_from_passphrase(passphrase)
        initialization_vector, encrypted_private_key = aes.encrypt(key, self.__get_private_key_bytes())

        file_name = f'private_key-{self._key_id}.pem'
        serialize(
            file_name=file_name,
            content=(
                salt,
                initialization_vector,
                encrypted_private_key
            ),
            directory_path=self._directory_path
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
        (salt, initialization_vector, encrypted_private_key) = deserialize(file_path)

        passphrase = input_password().encode('utf-8')

        aes = CryptographyAes()
        salt, key = aes.derive_key_from_passphrase(passphrase, salt)
        rsa_private_key = aes.decrypt(key, initialization_vector, encrypted_private_key)

        private_key = serialization.load_pem_private_key(
            rsa_private_key,
            password=None,
            backend=default_backend()
        )
        return private_key
