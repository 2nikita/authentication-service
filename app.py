from flask import Flask, request
import hashlib
import os
from uuid import uuid4
from datetime import datetime

from database import Database

DB = Database()

# based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def hash_password(password: str):
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


app = Flask(__name__)


@app.route("/create_user", methods=["POST"])
def create_user():
    # get login and password from request
    login = request.form.get("login")
    password = request.form.get("password")

    # hash user login and password
    login_key = hashlib.sha1(bytes(login, "utf-8")).hexdigest()
    password_salt, password_key = hash_password(password=password)
    used_id = str(uuid4())

    # add data to dict
    user_data = {
        "login_key": login_key,
        "password_salt": password_salt,
        "password_key": password_key,
        "user_id": used_id,
        "created_on": datetime.now(),
    }
    response = DB.write(data=user_data)
    return response


@app.route("/verify_user", methods=["POST"])
def verify_user():
    pass


# run app
if __name__ == "__main__":
    app.run(debug=True)
