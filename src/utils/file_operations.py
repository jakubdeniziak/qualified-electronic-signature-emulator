import os
import pickle


def save_to_file(file_name, content, directory_path=None):
    if directory_path is None:
        full_file_path = file_name
    else:
        full_file_path = os.path.join(directory_path, file_name)
    with open(full_file_path, 'wb') as file:
        file.write(content)


def serialize(file_name, content, directory_path=None):
    if directory_path is None:
        full_file_path = file_name
    else:
        full_file_path = os.path.join(directory_path, file_name)
    with open(full_file_path, 'wb') as file:
        pickle.dump(content, file)


def load_from_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def deserialize(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
    return data


def get_file_name_and_extension(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    return file_name, file_extension
