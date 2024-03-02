import json

from src.gui.window import TkWindow, choose_file


def encrypt():
    file_path = choose_file()
    print(file_path)


def decrypt():
    file_path = choose_file()
    print(file_path)


def sign():
    file_path = choose_file()
    print(file_path)


def check_signature():
    file_path = choose_file()
    print(file_path)


if __name__ == '__main__':
    window = TkWindow()

    with open('static/visual_identity.json', 'r') as file:
        visual_identity = json.load(file)

    app_name = visual_identity['name']
    width = visual_identity['width']
    height = visual_identity['height']
    background_color = visual_identity['background_color']

    labels_config = visual_identity['labels']
    buttons_config = visual_identity['buttons']

    window.set_title(app_name)
    window.set_size(width, height)
    window.set_background_color(background_color)

    window.add_label('QES', labels_config['heading'])
    window.add_label('Emulator', labels_config['subheading'])
    window.add_button('Encrypt', lambda: encrypt(), buttons_config['menu'])
    window.add_button('Decrypt', lambda: decrypt(), buttons_config['menu'])
    window.add_button('Sign', lambda: sign(), buttons_config['menu'])
    window.add_button('Check signature', lambda: check_signature(), buttons_config['menu'])
    window.add_button('Exit', lambda: window.exit(), buttons_config['menu'])

    window.init()
