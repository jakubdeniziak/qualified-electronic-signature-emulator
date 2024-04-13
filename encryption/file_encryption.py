from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from encryption.rsa import CryptographyRsa
from gui.window import choose_file, choose_directory
from utils.file_operations import load_from_file, get_file_name_and_extension, save_to_file


def generate_rsa_keys(gui_controller):
    directory_path = choose_directory('Choose directory to save keys')
    if directory_path is None:
        gui_controller.display_message('No directory selected')
        return
    CryptographyRsa().generate_keys(directory_path)


def encrypt_file(gui_controller):
    file_path = choose_file('Choose file to encrypt')
    if file_path is None:
        gui_controller.display_message('No file selected')
        return
    plaintext = load_from_file(file_path)

    public_key_path = choose_file('Choose public key')
    if file_path is None:
        gui_controller.display_message('No file selected')
        return
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


def decrypt_file(gui_controller):
    file_path = choose_file('Choose file to decrypt')
    if file_path is None:
        gui_controller.display_message('No file selected')
        return
    ciphertext = load_from_file(file_path)

    private_key_path = choose_file('Choose private key')
    if file_path is None:
        gui_controller.display_message('No file selected')
        return
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


def sign(gui_controller):
    file_path = choose_file(gui_controller)
    print(file_path)


def check_signature(gui_controller):
    file_path = choose_file(gui_controller)
    print(file_path)
