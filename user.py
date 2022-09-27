# User model
from ctypes import Union
import hashlib
import os
from uuid import uuid4
from datetime import datetime

from authentication import Authentication


class User:
    def __init__(self, db_instance):
        self.db_instance = db_instance

    def write(self, login: str, password: str):
        """Write new user to the database."""
        user_id = str(uuid4())
        created_on = datetime.now()
        login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
        password_salt, password_key = self._hash_password(password=password)

        query = f"""
            INSERT INTO user_data (user_id, login_key, password_key, password_salt, created_on)
            VALUES ('{user_id}', '{login_key}', '{password_key}', '{password_salt}', TIMESTAMP '{created_on}');
        """
        response = self.db_instance.execute(query=query)

        return response

    def verify(self, login: str, password: str):
        """Verify user data and, if it's valid, send JWT."""
        login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
        query = (
            "SELECT user_id, password_key, password_salt FROM user_data"
            + f" WHERE login_key = '{login_key}';"
        )
        result = self.db_instance.execute(query=query, result=True)
        if result:
            user_id, password_key, password_salt = (
                result[0][0],
                result[0][1],
                result[0][2],
            )

            hashed_password = self._generate_password(
                password=password, salt=password_salt
            )

            if password_key == hashed_password:
                authentication = Authentication(user_id=user_id)
                jwt_token = authentication.generate_token()

                return jwt_token
            else:
                return {"success": False}
        else:
            return {"success": False}

    # based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    @staticmethod
    def _hash_password(password: str):
        """Hash unencrypted password."""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt,
            iterations=100000,
        )
        salt_hex = salt.hex()
        key_hex = key.hex()
        return salt_hex, key_hex

    @staticmethod
    def _generate_password(password: str, salt: str) -> str:
        """Generate hashed password based on password value and salt."""
        byte_salt = bytes.fromhex(salt)

        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=byte_salt,
            iterations=100000,
        )
        key_hex = key.hex()
        return key_hex
