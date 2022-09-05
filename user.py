# User model
import hashlib
import os
from uuid import uuid4
from datetime import datetime


class User:
    def __init__(self, login: str, password: str):
        self.login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
        self.password_salt, self.password_key = self._hash_password(password)
        self.user_id = str(uuid4())
        self.created_on = datetime.now()

    def write(self, db_instance):
        query = f"""
            INSERT INTO user_data (user_id, login_key, password_key, password_salt, created_on)
            VALUES ('{self.user_id}', '{self.login_key}', '{self.login_key}', '{self.password_salt}', TIMESTAMP '{self.created_on}');
        """

        try:
            db_instance.cur.execute(query)
            db_instance.conn.commit()
            return {"success": True}
        except Exception as error:
            print("Oops! An exception has occured:", error)
            print("Exception TYPE:", type(error))
            return {"success": False}

    def verify():
        pass

    # based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    @staticmethod
    def _hash_password(password: str):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=salt,
            iterations=100000,
        )
        # convert from byte to hexadecimal format: reverse - bytes.fromhex('deadbeef')
        salt_hex = salt.hex()
        key_hex = key.hex()
        return salt_hex, key_hex
