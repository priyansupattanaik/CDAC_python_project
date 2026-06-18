import re


def validate_username(username):
    return bool(re.match(r"^[a-zA-Z0-9]{3,20}$", username))


def validate_password(password):
    return bool(re.match(r"^.{4,}$", password))


def validate_answer(ans):
    return bool(re.match(r"^[1-4]$", ans.strip()))