from abc import ABC, abstractmethod

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


class Aes(ABC):
    def __init__(self):
        self._LENGTH_OF_KEY_IN_BYTES = 32
        self._LENGTH_OF_SALT_IN_BYTES = 16
        self._LENGTH_OF_INITIALIZATION_VECTOR_IN_BYTES = 16
        self._ITERATIONS_FOR_KEY_DERIVATION = 100000

    @abstractmethod
    def derive_key_from_passphrase(self, passphrase):
        pass

    @abstractmethod
    def encrypt(self, key, data):
        pass

    @abstractmethod
    def decrypt(self, key, initialization_vector, data):
        pass

    @abstractmethod
    def _pad_data(self, data):
        pass

    @abstractmethod
    def _unpad_data(self, padded_data):
        pass


class CryptographyAes(Aes):
    def derive_key_from_passphrase(self, passphrase):
        salt = os.urandom(self._LENGTH_OF_SALT_IN_BYTES)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self._LENGTH_OF_KEY_IN_BYTES,
            salt=salt,
            iterations=self._ITERATIONS_FOR_KEY_DERIVATION,
            backend=default_backend()
        )
        key = kdf.derive(passphrase)
        return salt, key

    def encrypt(self, key, data):
        initialization_vector = os.urandom(self._LENGTH_OF_INITIALIZATION_VECTOR_IN_BYTES)
        padded_data = self._pad_data(data)
        encryptor = Cipher(algorithms.AES(key), modes.CBC(initialization_vector)).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return initialization_vector, ciphertext

    def decrypt(self, key, initialization_vector, data):
        decryptor = Cipher(algorithms.AES(key), modes.CBC(initialization_vector)).decryptor()
        padded_data = decryptor.update(data) + decryptor.finalize()
        data = self._unpad_data(padded_data)
        return data

    def _pad_data(self, data):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def _unpad_data(self, padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
        return unpadded_data
