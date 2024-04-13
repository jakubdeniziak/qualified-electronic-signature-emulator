from encryption.rsa import CryptographyRsa
from gui.window import choose_directory


def generate_rsa_keys():
    directory_path = choose_directory()
    CryptographyRsa().generate_keys(directory_path)
