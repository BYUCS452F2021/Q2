import os
import pickle


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
        raise "Invalid key"


def store(key, value):
    try:
        file = __key_to_file(key)
        with open(file, "wb") as f:
            data = pickle.dump(value, f)
    except:
        raise "Must provide a pickleable object"
