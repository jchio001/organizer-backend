from models import Account, session
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

import jwt_token_utils
import logging


def create_or_update_account(updated_account):
    existing_account = session \
        .query(Account) \
        .filter_by(google_id=updated_account.google_id) \
        .first()

    if not existing_account:
        try:
            logging.info("Account does not exist in the system!")
            session.add(updated_account)
            session.flush()
            session.commit()

            existing_account = updated_account
        except IntegrityError:
            session.rollback()
            logging.info('User already exists in the system!')

            existing_account = session \
                .query(Account) \
                .filter_by(google_id=updated_account.google_id) \
                .first()

    return {'token': jwt_token_utils.create_jwt_token(existing_account)}, HTTPStatus.OK
