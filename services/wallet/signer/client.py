import os
import sys
sys.path.insert(0, "../../depends/roll_up/pythonWrapper")
sys.path.insert(0, "../")

from flask import jsonify
from wallet import Wallet
from .web_service import WebService

rhs_leaf = os.environ["RHS_LEAF"]

class Client(object):
    def __init__(self, wallet, web_service):
        self.wallet = wallet
        self.web_service = web_service

    def sign_transfer(self, receiver_pub_key, token_id):
        msg = self.create_tx(receiver_pub_key)
        R, S = self.wallet.sign(msg)
        return jsonify(
            receiver_pub_key=receiver_pub_key,
            token_id=token_id,
            sig=[R, S]
        )

    def create_tx(self, receiver_pub_key):
        old_leaf = self.wallet.create_leaf(self.wallet.public_key, rhs_leaf)
        new_leaf = self.wallet.create_leaf(receiver_pub_key, rhs_leaf)
        return self.wallet.hash_padded(old_leaf, new_leaf)[2:]

    def verify_proof(self, root, token_id, proof):
        pass