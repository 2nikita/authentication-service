from flask import Flask, request
import hashlib
import os
from uuid import uuid4
from datetime import datetime

from database import Database
from authentication import Authentication

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


def generate_password(salt: str, password: str):
    # get the salt from DB to generate password
    # then compare it with the one sent when authenticating
    byte_salt = bytes.fromhex(salt)
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=byte_salt,
        iterations=100000,
    )
    key_hex = key.hex()
    return key_hex


app = Flask(__name__)
# TODO: use middleware - https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4


@app.route("/create_user", methods=["POST"])
def create_user():
    # get login and password from request
    login = request.form.get("login")
    password = request.form.get("password")

    # hash user login and password
    login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
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


@app.route("/authenticate_user", methods=["GET"])
def authenticate_user():
    login = request.headers.get("login")
    password = request.headers.get("password")

    # hash user login and get password data from DB
    login_key = hashlib.sha1(login.encode("utf-8")).hexdigest()
    import pdb

    pdb.set_trace()
    data = Database().get_user_data(user_login=login_key)
    hashed_password = generate_password(
        salt=data["password_salt"], password=password
    )
    if data["password_key"] == hashed_password:
        authentication = Authentication(user_id=data["user_id"])
        jwt_token = authentication.generate_token()

        return jwt_token
    else:
        return {"success": False}


# run app
if __name__ == "__main__":
    app.run(debug=True)
