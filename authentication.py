from datetime import datetime
import jwt
from flask import request, redirect
from database import Database
from functools import wraps

EXPIRATION_TIMEFRAME_SC = 1800  # TODO: set it as env var?
JWT_SECRET = "kaef"  # TODO: set it as env var?


class Authentication:
    def __init__(self, user_id):
        self.iss = "Authentication Server"
        self.iat = datetime.now().timestamp()
        self.sub = user_id
        self.exp = self.iat + EXPIRATION_TIMEFRAME_SC

    def generate_token(self):
        encoded_jwt = jwt.encode(
            payload=self.__dict__, key=JWT_SECRET, algorithm="HS256"
        )
        return encoded_jwt


def verify_token(route):
    @wraps(route)
    def verify():
        token = request.headers.get("authorization").split(" ")[1]
        try:
            payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms="HS256")
        except jwt.ExpiredSignatureError as error:
            # check refresh token
            print(error)
            return redirect("/authenticate_user")
        user_id = payload["sub"]
        check_user = Database().execute(
            f"SELECT COUNT(*) FROM user_data WHERE user_id = '{user_id}';",
            result=True,
        )
        if check_user[0][0] == 1:
            return route
        else:
            return {"status": "User doesn't exist"}  # redirect to login?

    return verify
