from gui.config_functions import usb_drive_icon_config
from gui.initializer import GuiInitializer
from gui.window import TkWindow
from encryption.file_encryption import generate_rsa_keys


class TkInitializer(GuiInitializer):
    def __init__(self):
        super().__init__()
        self._window = TkWindow()
        self._load_config()
        self._set_window_params()
        self._add_content()

    def initialize(self):
        self._window.init()

    def _set_window_params(self):
        self._window.set_title(self._config['name'])
        self._window.set_size(self._config['width'], self._config['height'])
        self._window.set_background_color(self._config['background_color'])

    def _add_content(self):
        labels_config = self._config['labels']
        buttons_config = self._config['buttons']

        self._window.add_label('QES Emulator', labels_config['heading'])
        self._window.add_label('Key generation', labels_config['subheading'])

        self._window.add_button('Generate RSA Keys', lambda: generate_rsa_keys(), buttons_config['menu'])
        self._window.add_button('Exit', lambda: self._window.exit(), buttons_config['menu'])

        self._window.add_icon('../../gui/static/pen-drive-icon.png', buttons_config['menu_icon'],
                              usb_drive_icon_config())
