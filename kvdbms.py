import os
import pickle


def __key_to_file(key: str):
    filepath = key.replace(':', '/')
    directory, file = os.path.split(filepath)
    os.makedirs(directory, exist_ok=True)
    return filepath


def get(key):
    file = __key_to_file(key)
    with open(file, "rb") as f:
        return pickle.load(f)


def store(key, value):
    try:
        file = __key_to_file(key)
        with open(file, "wb") as f:
            data = pickle.dump(value, f)
    except:
        raise "Must provide a pickleable object"
