import hashlib
import os
from datetime import datetime

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from encryption.rsa import CryptographyRsa
from gui.window import choose_file, choose_directory
from utils.file_operations import load_from_file, get_file_name_and_extension, save_to_file, get_document_data
from utils.xml_handler import create_xml


def compute_document_hash(document_path):
    document_content = load_from_file(document_path)
    document_hash = hashlib.sha256(document_content).hexdigest()
    return document_hash


def generate_rsa_keys(gui_controller):
    directory_path = choose_directory('Choose directory to save keys')
    if directory_path is None:
        gui_controller.display_message('No directory selected')
        return
    try:
        CryptographyRsa().generate_keys(directory_path)
    except Exception as e:
        gui_controller.display_message(e)
        return
    gui_controller.display_message('Keys generated')


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
    file_path = choose_file('Choose file to sign')

    file_size, file_extension, modification_date = get_document_data(file_path)
    username = os.getlogin()
    timestamp = datetime.now()

    file_hash = compute_document_hash(file_path)

    private_key_path = choose_file('Choose private key')
    if private_key_path is None:
        gui_controller.display_message('No private key selected')
        return

    private_key = CryptographyRsa.load_private_key(private_key_path)

    encrypted_file_hash = private_key.sign(
        bytes(file_hash.encode('utf-8')),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    tags = {
        'FileSize': file_size,
        'FileExtension': file_extension,
        'ModificationDate': modification_date,
        'DocumentHash': encrypted_file_hash,
        'UserInfo': username,
        'Timestamp': timestamp
    }

    xml_data = bytes(create_xml(tags).encode('utf-8'))
    save_to_file('signature.xml', xml_data)


def check_signature(gui_controller):
    file_path = choose_file(gui_controller)
    print(file_path)
