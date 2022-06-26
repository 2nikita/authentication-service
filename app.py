from flask import Flask, request
import hashlib
import os
from uuid import uuid1
from datetime import datetime

from database import Database

# based on https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
def hash_password(password: str):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=100000,
    )
    return salt, key


app = Flask(__name__)


@app.route("/create_user", methods=["POST"])
def create_user():
    # get login and password from request
    login = request.form.get("login")
    password = request.form.get("password")

    # hash user login and password
    login_key = hashlib.sha1(bytes(login, "utf-8")).digest()
    password_salt, password_key = hash_password(password=password)
    used_id = str(uuid1())

    # add data to dict
    user_data = {
        "login_key": login_key,
        "password_salt": password_salt,
        "password_key": password_key,
        "user_id": used_id,
        "created_on": datetime.now(),
    }
    import pdb

    pdb.set_trace()
    return login


# run app
if __name__ == "__main__":
    app.run(debug=True)
