"""
Xena - Smart city solutions.

title          : models.py
description    : Defines the models to store blocks for transactions.
author         : Surya Saini
email          : sainisurya.1@gmail.com
created_at     : 2019-06-23
"""

# import defualt modules
import sys, os

# import functions from sqlalchemy package
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Table,
    Text,
    ForeignKey,
    Date,
    DateTime,
    BOOLEAN,
    BigInteger
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import and_, or_
from sqlalchemy.sql.expression import true
from sqlalchemy.ext.declarative import declarative_base

# import User class from xena
sys.path.append("../")
from xena.models import User

# Define engine, session to interact with postgresql blockchain db
engine = create_engine("postgresql+psycopg2://surya:stein@localhost/conduent_blockchain")
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# Define engine, session to interact with postgresql user db
engine_xena = create_engine("postgresql+psycopg2://surya:stein@localhost/conduent")
Base_xena = declarative_base()
Session_xena = sessionmaker(bind=engine_xena)
Session_xena.configure(bind=engine_xena)
session_xena = Session_xena()


# define transaction block
class Block(Base):
    """ Model storing the transaction block information for a user.
    """

    __tablename__ = 'block'

    id = Column(
        'id',
        Integer,
        primary_key=True,
        autoincrement=True
    )
    timestamp = Column(
        'timestamp',
        DateTime()
    )
    transaction_sender_id = Column(
        'transaction_user_id',
        Integer
    )
    transaction_recipient_id = Column(
        'transaction_recipient_id',
        Integer
    )
    transaction_amount = Column(
        'transaction_amount',
        Integer
    )
    proof = Column(
        'proof',
        String(255)
    )
    previous_hash = Column(
        'previous_hash',
        String(255)
    )

    # define Post model methods
    def __init__(self, **kwargs):
        super(Block, self).__init__(**kwargs)

    def create(self):
        """ Add new block to blockchain.
        """
        session.add(self)
        session.commit()

    def get_last(self):
        """ Get the last block of the chain.
        """
        return session.query(Block).order_by(Block.id.desc()).first()


class Miner():
    """ Defines the class for miners/users registered with Xena.
    """

    def login(self, username, password):
        """ Logs in a user.

        :param username: Username for the user to be logged in.
        :param type: String
        :param password: Password for the logged in your.
        :param type: String
        """
        return session_xena.query(User).filter(and_(User.username == username,User.password == password )).first()
