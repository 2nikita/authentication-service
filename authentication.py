from datetime import datetime
import jwt
from flask import request, redirect
from database import Database
from functools import wraps
from uuid import uuid4

EXPIRATION_TIMEFRAME_AT = 1800  # TODO: set it as env var
EXPIRATION_TIMEFRAME_RT = 86400  # TODO: set it as env var
ACCESS_TOKEN_SECRET = "kaef"  # TODO: set it as env var
REFRESH_TOKEN_SECRET = "antikaef"  # TODO: set it as env var


class Authentication:
    def __init__(self, user_id):
        self.iss = "Authentication Server"
        self.iat = datetime.now().timestamp()
        self.sub = user_id
        self.exp = self.iat + EXPIRATION_TIMEFRAME_AT

    def generate_tokens(self) -> dict:
        access_token = jwt.encode(
            payload=self.__dict__, key=ACCESS_TOKEN_SECRET, algorithm="HS256"
        )
        refresh_token = str(uuid4())  # TODO: set it as JWT
        return {"access_token": access_token, "refresh_token": refresh_token}


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
