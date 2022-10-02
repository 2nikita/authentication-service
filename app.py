from flask import Flask, request, make_response

from user import User
from middleware import verify_token

app = Flask(__name__)
# TODO: use middleware - https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4


@app.route("/create_user", methods=["POST"])
def create_user():
    # get login and password from request
    # TODO: handle errors
    login = request.form.get("login")
    password = request.form.get("password")

    # write user data to db
    # TODO: handle posssible errors - duplicated login, etc. (db side?)
    user = User()
    response = user.write(login=login, password=password)

    return response


@app.route("/authenticate_user", methods=["GET"])
def authenticate_user():
    # TODO: handle errors
    login = request.headers.get("login")
    password = request.headers.get("password")
    user = User()
    # get JWT if user data is valid
    tokens = user.verify(login=login, password=password)
    response = make_response()
    response.set_cookie("access_token", tokens["access_token"])
    response.set_cookie("refresh_token", tokens["refresh_token"])
    return response


@app.route("/create_ad", methods=["POST"])
@verify_token
def create_ad():
    return {"Do smth": "blabla"}


# run app
if __name__ == "__main__":
    app.run(debug=True)
