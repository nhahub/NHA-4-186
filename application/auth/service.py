from application.auth.validator import (
    validate_registration,
    validate_login
)

from application.auth.password import (
    hash_password,
    verify_password
)

from database.queries import (
    create_user,
    get_user_by_username
)


class AuthService:

    # ==============================
    # Register
    # ==============================

    def register(
        self,
        full_name,
        username,
        email,
        password,
        role
    ):

        valid, message = validate_registration(
            full_name,
            username,
            email,
            password,
            role
        )

        if not valid:
            return False, message

        hashed_password = hash_password(password)

        success = create_user(
            full_name,
            username,
            email,
            hashed_password,
            role
        )

        if success:
            return True, "Account created successfully."

        return False, "Username or Email already exists."

    # ==============================
    # Login
    # ==============================

    def login(self, username, password):

        valid, message = validate_login(
            username,
            password
        )

        if not valid:
            return False, message

        user = get_user_by_username(username)

        if user is None:
            return False, "Invalid username or password."

        if not verify_password(
            password,
            user["password"]
        ):
            return False, "Invalid username or password."

        return True, user