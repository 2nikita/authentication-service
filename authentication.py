from datetime import datetime
import jwt


EXPIRATION_TIMEFRAME_AT = 1800  # TODO: set it as env var
EXPIRATION_TIMEFRAME_RT = 86400  # TODO: set it as env var
ACCESS_TOKEN_SECRET = "kaef"  # TODO: set it as env var
REFRESH_TOKEN_SECRET = "antikaef"  # TODO: set it as env var


class Authentication:

    iss = "Authentication Server"
    iat = datetime.now().timestamp()

    def __init__(self, user_id):
        self.payload = {
            "access_token": {
                "iss": self.iss,
                "iat": self.iat,
                "sub": user_id,
                "exp": self.iat + EXPIRATION_TIMEFRAME_AT,
            },
            "refresh_token": {
                "iss": self.iss,
                "iat": self.iat,
                "sub": user_id,
                "exp": self.iat + EXPIRATION_TIMEFRAME_RT,
            },
        }

    def generate_tokens(self) -> dict:
        access_token = jwt.encode(
            payload=self.payload["access_token"],
            key=ACCESS_TOKEN_SECRET,
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            payload=self.payload["refresh_token"],
            key=REFRESH_TOKEN_SECRET,
            algorithm="HS256",
        )
        return {"access_token": access_token, "refresh_token": refresh_token}
