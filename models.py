from sqlalchemy import  Column, create_engine, DateTime, Integer, Numeric, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import os

db_url = os.environ['FOOD_ORGANIZER_DB_URI']
db = create_engine(db_url)
base = declarative_base()


class Account(base):
    __tablename__ = 'account'

    id = Column(Integer, Sequence('user_id_seq', start=1, increment=1), primary_key=True)
    google_id = Column(Numeric, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    profile_photo = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    def to_json(self):
        return {'id': self.id,
                'google_id': self.google_id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'profile_photo': self.profile_photo}


# Sets up a sqlalchemy session
Session = sessionmaker(db)
session = Session()


# This allows you to run models.py to create the tables!
if __name__ == "__main__":
    base.metadata.create_all(db)