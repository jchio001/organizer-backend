from decorators import ValidateGoogleIdToken
from flask import Flask

import account_client
import json
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['PUT'])
@ValidateGoogleIdToken
def connect_with_google(*args, **kwargs):
    response_dict, status_code = account_client.create_or_update_account(kwargs.get('account'))
    return json.dumps(response_dict), status_code


# Since everything that we return will literally be a json, might as well use @app.after_request
# instead of attaching a custom annotation (aka decorators in Python land)
@app.after_request
def set_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run()