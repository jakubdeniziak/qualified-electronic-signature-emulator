from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from src.encryption.rsa import CryptographyRsa
from src.gui.window import choose_file, choose_directory
from src.utils.file_operations import load_from_file, get_file_name_and_extension, save_to_file


def generate_rsa_keys():
    directory_path = choose_directory()
    CryptographyRsa().generate_keys(directory_path)


def encrypt_file():
    file_path = choose_file('Choose file to encrypt')
    plaintext = load_from_file(file_path)

    public_key_path = choose_file('Choose public key')
    public_key = CryptographyRsa.load_public_key(public_key_path)

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
    save_to_file(encrypted_file_name, ciphertext)


def decrypt_file():
    file_path = choose_file('Choose file to decrypt')
    ciphertext = load_from_file(file_path)

    private_key_path = choose_file('Choose private key')
    private_key = CryptographyRsa.load_private_key(private_key_path)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    file_name, file_extension = get_file_name_and_extension(file_path)
    decrypted_file_name = f'{file_name}_decrypted{file_extension}'
    save_to_file(decrypted_file_name, plaintext)


def sign():
    file_path = choose_file()
    print(file_path)


def check_signature():
    file_path = choose_file()
    print(file_path)
