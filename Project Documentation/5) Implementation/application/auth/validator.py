import re


def validate_registration(
    full_name,
    username,
    email,
    password,
    role
):

    if not full_name.strip():
        return False, "Full Name is required."

    if not username.strip():
        return False, "Username is required."

    if not email.strip():
        return False, "Email is required."

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        return False, "Invalid email."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    if role not in ["Admin", "Engineer"]:
        return False, "Invalid role."

    return True, "Valid"


def validate_login(username, password):

    if not username.strip():
        return False, "Username is required."

    if not password.strip():
        return False, "Password is required."

    return True, "Valid"
