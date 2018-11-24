from flask import request, jsonify
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
from http import HTTPStatus
from jwt import DecodeError
from models import Account

import account_client
import jwt_token_utils
import logging
import os
import time

google_server_client_id = os.environ['FOOD_ORGANIZER_GOOGLE_SERVER_CLIENT_ID']


def ValidateGoogleIdToken(f):
    @wraps(f)
    def validate_google_id_token(*args, **kwargs):
        google_id_token = request.args.get('google_id_token')

        if not google_id_token:
            response = jsonify({'error': 'google_id_token not present.'})
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        try:
            id_token_info = id_token.verify_oauth2_token(google_id_token, requests.Request(), google_server_client_id)
            logging.info(id_token_info)
        except ValueError as e:
            response = jsonify({'error': str(e)})
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response

        if id_token_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com'] \
            or id_token_info['aud'] != google_server_client_id:
            logging.info(id_token_info['aud'])
            response = jsonify({'error': 'google_id_token from invalid client.'})
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        return f(*args, **kwargs, account=Account(google_id=id_token_info.get('sub'),
                                                  first_name=id_token_info.get('given_name'),
                                                  last_name=id_token_info.get('family_name'),
                                                  email = id_token_info.get('email'),
                                                  profile_photo = id_token_info.get('picture')))

    return validate_google_id_token


def ValidateJwtToken(f):
    @wraps(f)
    def validate_jwt_token(*args, **kwargs):
        jwt_token = request.headers.get('authorization')

        if not jwt_token:
            response = jsonify({'error': 'Token not present.'})
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        try:
            jwt_token_info = jwt_token_utils.decode_jwt_token(jwt_token)
        except DecodeError:
            response = jsonify({'error': 'Invalid token supplied.'})
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response

        account = account_client.get_account(jwt_token_info.get('sub'))
        if not account:
            response = jsonify({'error': 'Associated account does not exist.'})
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response

        now = int(time.time())
        if jwt_token_info.get('exp') < now:
            response = jsonify({'error': 'Expired token.'})
            response.status_code = HTTPStatus.UNAUTHORIZED
            return response

        return f(*args, **kwargs, account=account)

    return validate_jwt_token
