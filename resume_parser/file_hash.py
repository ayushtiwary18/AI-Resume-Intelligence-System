import hashlib


def calculate_file_hash(file_data):
    sha256 = hashlib.sha256()

    sha256.update(file_data)

    return sha256.hexdigest()