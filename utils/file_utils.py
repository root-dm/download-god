import hashlib


def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def truncate_text(text, max_length=15):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
