from flask import request, abort, make_response
from datetime import datetime
import jwt
from functools import wraps

from user import User
from authentication import Authentication

EXPIRATION_TIMEFRAME_AT = 1800  # TODO: set it as env var
EXPIRATION_TIMEFRAME_RT = 86400  # TODO: set it as env var
ACCESS_TOKEN_SECRET = "kaef"  # TODO: set it as env var
REFRESH_TOKEN_SECRET = "antikaef"  # TODO: set it as env var


def verify_token(route):
    @wraps(route)
    def verify():
        access_token = request.cookies.get("access_token")
        print(f"Got access token: {access_token} \n")
        if not access_token:
            return {
                "message": "Authentication failed: no access token provided."
            }, 500

        payload_at = jwt.decode(
            jwt=access_token,
            key=ACCESS_TOKEN_SECRET,
            algorithms="HS256",
            options={"verify_signature": False},
        )
        now = datetime.now().timestamp()
        if now - payload_at["iat"] > EXPIRATION_TIMEFRAME_AT:
            refresh_token = request.cookies.get("refresh_token")
            print(f"Got refresh token: {refresh_token} \n")
            if not refresh_token:
                return {
                    "message": "Authentication failed: no refresh token provided."
                }, 500
            payload_rt = jwt.decode(
                jwt=refresh_token,
                key=REFRESH_TOKEN_SECRET,
                algorithms="HS256",
                options={"verify_signature": False},
            )
            if now - payload_rt["iat"] > EXPIRATION_TIMEFRAME_RT:
                # TODO: redirect to authentication? but the user is not checkec
                abort(403)
            else:
                if not check_user(id=payload_rt["sub"]):
                    return {
                        "message": "Authentication failed: user doesn't exist."
                    }, 500

                print("Generate new tokens")
                authentication = Authentication(user_id=payload_rt["sub"])
                tokens = authentication.generate_tokens()
                print(f"Generated tokens: {tokens}")

                response = make_response()
                response.set_cookie("access_token", tokens["access_token"])
                response.set_cookie("refresh_token", tokens["refresh_token"])

                return route(response)
        else:
            if not check_user(id=payload_at["sub"]):
                return {
                    "message": "Authentication failed: user doesn't exist."
                }, 500

            return route(make_response())

    return verify


def check_user(id: str) -> bool:
    """Check if user exists."""
    is_user = User().is_user(id=id)
    return is_user
