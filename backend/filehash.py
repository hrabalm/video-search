from pydantic import BaseModel
from simple_file_checksum import get_checksum


class FileHash(BaseModel):
    filename: str
    hash_function: str
    checksum: str


def file_hash(filename, hash_function="SHA256") -> FileHash:
    checksum = get_checksum(filename, hash_function)
    return FileHash(
        filename=filename,
        hash_function=hash_function,
        checksum=checksum,
    )
