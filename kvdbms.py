import os
import pickle


class InvalidKeyExpection(Exception):
    pass


class UnpicklableObjectException(Exception):
    pass


def __key_to_file(key: str):
    filepath = ".kvdbmsstore/" + key.replace(':', '/')
    directory, file = os.path.split(filepath)
    os.makedirs(directory, exist_ok=True)
    return filepath


def get(key):
    try:
        file = __key_to_file(key)
        with open(file, "rb") as f:
            return pickle.load(f)
    except:
        raise InvalidKeyExpection


def store(key, value):
    try:
        file = __key_to_file(key)
        with open(file, "wb") as f:
            data = pickle.dump(value, f)
    except:
        raise UnpicklableObjectException
