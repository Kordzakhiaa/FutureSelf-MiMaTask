import json
import re

from passlib.handlers.sha2_crypt import sha256_crypt


def is_valid_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False


def check_email(email: str) -> bool:
    with open('user_data.json', 'r+') as f:
        json_data = json.load(f)
    for data in json_data:
        if email in data.values():
            return True
    return False


def is_valid_password(password: str) -> bool:
    reg = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$'
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat and len(password) >= 8:
        return True
    return False


def check_password(password: str) -> bool:
    with open('user_data.json', 'r+') as f:
        json_data = json.load(f)
    for data in json_data:
        hashed_password = data['password1']
        if sha256_crypt.verify(password, hashed_password):
            return True
    return False
