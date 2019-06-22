"""
Xena - Smart city solutions.

title          : views.py
description    : Defines the views to mine blocks for transactions.
author         : Surya Saini
email          : sainisurya.1@gmail.com
created_at     : 2019-06-23
"""

# import defualt module
import hashlib
import json
import os
import sys

from datetime import datetime
from uuid import uuid4

# import modules from flask
from flask import url_for, redirect
from flask import session as flask_session
from flask import (
    request,
    render_template,
    Response,
    abort,
    jsonify
)

# import modules from self created classes
from models import Block, Miner
from app import app
sys.path.append("../")
from xena.models import (
    User,
    UserWallet,
    UtilityItemUser
)


# define Blockchain
class Blockchain(object):
    """ Implement the basic structure of Xena's transaction blockchain.
    """

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        if Block().get_last() is None:
            self.create_genesis_block()

    def create_genesis_block(self):
        """ Create a genesis block.
        """

        self.new_block(transaction_sender_id=0, transaction_recipient_id=0, amount=0, prev_hash=1, proof=100)

    def new_block(self, transaction_sender_id, transaction_recipient_id, amount, proof, prev_hash=None):
        """ Adds a new block to the blockchain.

        :param transaction_sender_id: Id of the user who initiated the transaction.
        :param type: int
        :param transaction_recipient_id: Id of the user who recieved the transaction.
        :param type: int
        :param amount: Amount of money used in transaction
        :param type: int
        :param prev_hash: Hash of the previous transaction
        :param type: String
        :param proof: Proof of work for the transaction.
        :param type: String
        """
        
        block = Block(
            timestamp=datetime.now(),
            transaction_sender_id=transaction_sender_id,
            transaction_recipient_id=transaction_recipient_id,
            transaction_amount=amount,
            proof=proof,
            previous_hash=prev_hash
        )
        self.current_transactions = []
        block.create()

    def new_transaction(self, transaction_sender_id, transaction_recipient_id, amount):
        """ Creates a new transaction to go into the next mined Block.

        :param transaction_sender_id: Id of the user who initiated the transaction.
        :param type: int
        :param transaction_recipient_id: Id of the user who recieved the transaction.
        :param type: int
        :param amount: Amount of money used in transaction
        :param type: int
        """

        self.current_transactions.append({
            'transaction_sender_id': transaction_sender_id,
            'amount': amount,
            'transaction_recipient_id': transaction_recipient_id
        })

        return "transaction added"

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# define functions for the client
@app.route('/', methods=['GET'])
def index():
    """ Renders the login user template.
    """
    
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """ login a user.
    """

    if request.method == 'POST':
        data = request.form
        miner = Miner().login(data['username'], data['password'])
        if miner :
            flask_session['miner_id'] = miner.id
            return redirect(
                url_for('mine_panel')
            )
        else:
            return "You are not a registered user."


@app.route('/mine', methods=['GET'])
def  mine_panel():
    """ Render the mining panel.
    """
    
    return render_template('mine_panel.html')


@app.route('/mine/block', methods=['POST'])
def mine_block():
    """ Mines a new block for the block chain.
    """
    if request.method == 'POST':
        data = request.form
        blockchain = Blockchain()
        blockchain.new_transaction(
            data['transaction_sender_id'],
            data['transaction_recipient_id'],
            data['amount']
        )
        last_proof = Block().get_last().proof

        proof = blockchain.proof_of_work(last_proof)
        prev_hash = Block().get_last().previous_hash
        
        blockchain.new_block(
            data['transaction_sender_id'],
            data['transaction_recipient_id'],
            data['amount'],
            proof,
            prev_hash
        )

        # register the transation
        UtilityItemUser().register(data['transaction_id'])
        # Add virtual value to the miner
        miner_id = flask_session.get('miner_id')
        UserWallet().successful_mine(miner_id) 
    
    return "Block successfully mined."


if __name__ == "__main__":
    app.run(port=7000)
