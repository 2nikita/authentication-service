# User model
import hashlib
import os
from uuid import uuid4
from datetime import datetime

from authentication import Authentication


class User:
    def __init__(self, login: str, password: str, db_instance):
        self.login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
        self.password = password
        self.db_instance = db_instance

    def write(self):
        """Write new user to the database."""
        user_id = str(uuid4())
        created_on = datetime.now()
        password_salt, password_key = self._hash_password()

        query = f"""
            INSERT INTO user_data (user_id, login_key, password_key, password_salt, created_on)
            VALUES ('{user_id}', '{self.login_key}', '{password_key}', '{password_salt}', TIMESTAMP '{created_on}');
        """
        response = self.db_instance.execute(query=query)

        return response

    def verify(self):
        """Verify user data and, if it's valid, send JWT."""
        query = (
            "SELECT user_id, password_key, password_salt FROM user_data"
            + f" WHERE login_key = '{self.login_key}';"
        )
        result = self.db_instance.execute(query=query, result=True)
        if result:
            user_id, password_key, password_salt = (
                result[0][0],
                result[0][1],
                result[0][2],
            )

            hashed_password = self._generate_password(salt=password_salt)

            if password_key == hashed_password:
                authentication = Authentication(user_id=user_id)
                jwt_token = authentication.generate_token()

                return jwt_token
            else:
                return {"success": False}
        else:
            return {"success": False}

    # based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    def _hash_password(self):
        """Hash unencrypted password."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=self.password.encode("utf-8"),
            salt=salt,
            iterations=100000,
        )
        salt_hex = salt.hex()
        key_hex = key.hex()
        return salt_hex, key_hex

    def _generate_password(self, salt: str) -> str:
        """Generate hashed password based on password value and salt."""
        byte_salt = bytes.fromhex(salt)

        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=self.password.encode("utf-8"),
            salt=byte_salt,
            iterations=100000,
        )
        key_hex = key.hex()
        return key_hex
