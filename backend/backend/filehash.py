from simple_file_checksum import get_checksum


def file_hash(filename, hash_function="SHA256") -> str:
    checksum = get_checksum(filename, hash_function)
    return checksum
