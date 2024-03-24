from datetime import datetime

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from src.encryption.rsa import load_public_key
from src.gui.window import choose_file


def encrypt_file():
    file_path = choose_file()
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    public_key_path = choose_file()
    public_key = load_public_key(public_key_path)

    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    now_hash = hash(datetime.now())
    file_name = f'public_key-{now_hash}'
    with open(file_name, 'wb') as file:
        file.write(ciphertext)


def decrypt_file():
    file_path = choose_file()
    print(file_path)


def sign():
    file_path = choose_file()
    print(file_path)


def check_signature():
    file_path = choose_file()
    print(file_path)