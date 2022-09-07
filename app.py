from flask import Flask, request

from database import Database
from user import User

app = Flask(__name__)
# TODO: use middleware - https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4


@app.route("/create_user", methods=["POST"])
def create_user():
    # get login and password from request
    login = request.form.get("login")
    password = request.form.get("password")

    # write user data to db
    # TODO: handle posssible errors - duplicated login, etc.
    user = User(login=login, password=password, db_instance=Database())
    response = user.write()

    return response


@app.route("/authenticate_user", methods=["GET"])
def authenticate_user():
    login = request.headers.get("login")
    password = request.headers.get("password")
    user = User(login=login, password=password, db_instance=Database())
    # get JWT if user data is valid
    response = user.verify()
    return response


# run app
if __name__ == "__main__":
    app.run(debug=True)
