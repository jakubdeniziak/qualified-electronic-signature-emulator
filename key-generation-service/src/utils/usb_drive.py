import pyudev


def is_usb_drive_connected():
    context = pyudev.Context()
    devices = context.list_devices(subsystem='block', DEVTYPE='disk')
    for device in devices:
        if 'ID_BUS' in device and device['ID_BUS'] == 'usb':
            return True
    return False
