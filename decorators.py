from flask import request, jsonify
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests
from http import HTTPStatus
from models import Account

import logging
import os

google_server_client_id = os.environ['FOOD_ORGANIZER_GOOGLE_SERVER_CLIENT_ID']


def ValidateGoogleIdToken(f):
    @wraps(f)
    def validate_user(*args, **kwargs):
        google_id_token = request.args.get('google_id_token')

        if not google_id_token:
            response = jsonify({'error': 'google_id_token not present.'})
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        id_token_info = id_token.verify_oauth2_token(google_id_token, requests.Request(), google_server_client_id)
        logging.info(id_token_info)

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

    return validate_user
