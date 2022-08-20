from datetime import datetime
import jwt

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
