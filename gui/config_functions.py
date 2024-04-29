from utils.usb_drive import is_usb_drive_connected


def usb_drive_icon_config():
    if is_usb_drive_connected() is False:
        return {'bg': 'red'}
    return {'bg': 'green'}
