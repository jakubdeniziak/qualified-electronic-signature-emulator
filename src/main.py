from src.encryption.rsa import CryptographyRsa
from src.gui.initializer import TkInitializer


if __name__ == '__main__':
    rsa = CryptographyRsa()
    rsa.generate_keys()

    gui_initializer = TkInitializer()
    gui_initializer.initialize()
