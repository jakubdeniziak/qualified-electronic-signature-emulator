import os


def save_to_file(file_name, content):
    with open(file_name, 'wb') as file:
        file.write(content)


def save_multiple_to_file(file_name, content):
    with open(file_name, 'wb') as file:
        for chunk in content:
            file.write(chunk)


def load_from_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def get_file_name_and_extension(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    return file_name, file_extension
