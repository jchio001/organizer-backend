from decorators import ValidateGoogleIdToken, ValidateJwtToken
from flask import Flask, request
from http import HTTPStatus

import account_client
import json
import jwt_token_utils
import logging
import places_client

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['POST'])
@ValidateGoogleIdToken
def connect_with_google(*args, **kwargs):
    response_dict, status_code = account_client.create_or_update_account(kwargs.get('account'))
    return json.dumps(response_dict), status_code


@app.route('/token')
@ValidateJwtToken
def exchange_token(*args, **kwargs):
    response_dict = {'token': jwt_token_utils.create_jwt_token(kwargs.get('account'))}
    return json.dumps(response_dict), HTTPStatus.OK


@app.route('/places', methods=['GET'])
@ValidateJwtToken
def get_places():
    response_dict, status_code = places_client.get_places(query_string=request.args.get('input'),
                                                          location=request.args.get('location'))
    return json.dumps(response_dict), status_code


# Since everything that we return will literally be a json, might as well use @app.after_request
# instead of attaching a custom annotation (aka decorators in Python land)
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run()