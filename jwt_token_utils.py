import jwt
import os
import time

jwt_secret = os.environ['FOOD_ORGANIZER_JWT_SECRET']


# For now, let's make the token expire after 30 days.
def create_jwt_token(account):
    token_creation = int(time.time())
    token_expiration = token_creation + 2592000
    return jwt.encode({'id': account.id, 'iat': token_creation, 'exp': token_expiration},
                      jwt_secret,
                      algorithm='HS512')\
        .decode('utf-8')


# Decodes a token and returns the user id if the token is valid
def decode_jwt_token(token):
    return jwt.decode(token.encode('utf-8'), jwt_secret, algorithms=['HS512'])