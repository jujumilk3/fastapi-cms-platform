import json
import random
import string


def is_json(json_to_check: bytes):
    try:
        json.loads(json_to_check)
    except ValueError:
        return False
    return True


def random_hash(length: int = 12):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
