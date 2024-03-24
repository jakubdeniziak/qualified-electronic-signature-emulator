import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from src.encryption.rsa import load_public_key, load_private_key
from src.gui.window import choose_file


def get_file_name_and_extension(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    return file_name, file_extension


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

    file_name, file_extension = get_file_name_and_extension(file_path)
    encrypted_file_name = f'{file_name}_encrypted{file_extension}'
    with open(encrypted_file_name, 'wb') as file:
        file.write(ciphertext)


def decrypt_file():
    file_path = choose_file()
    with open(file_path, 'rb') as file:
        ciphertext = file.read()

    private_key_path = choose_file()
    private_key = load_private_key(private_key_path)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    file_name, file_extension = get_file_name_and_extension(file_path)
    with open(f'{file_name}_decrypted{file_extension}', 'wb') as file:
        file.write(plaintext)


def sign():
    file_path = choose_file()
    print(file_path)


def check_signature():
    file_path = choose_file()
    print(file_path)
