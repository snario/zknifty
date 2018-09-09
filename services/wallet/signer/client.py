import os
import sys
sys.path.insert(0, "../../depends/roll_up/pythonWrapper")
sys.path.insert(0, "../")

from flask import jsonify
from wallet import Wallet
from .web_service import WebService

class Client(object):
    def __init__(self, wallet, web_service):
        self.wallet = wallet
        self.web_service = web_service

    def sign_transfer(self, receiver_pub_key, token_id):
        msg = self.create_tx(receiver_pub_key, token_id)
        R, S = self.wallet.sign(msg)
        return jsonify(
            receiver_pub_key=receiver_pub_key,
            token_id=token_id,
            sig=[R, S]
        )

    def create_tx(self, receiver_pub_key, token_id):
        rhs_leaf = self.wallet.create_rhs_leaf(token_id)
        old_leaf = self.wallet.create_leaf(self.wallet.public_key, rhs_leaf)
        new_leaf = self.wallet.create_leaf(receiver_pub_key, rhs_leaf)
        return self.wallet.hash_padded(old_leaf, new_leaf)[2:]

    def verify_proof(self, root, token_id, proof):
        assert(len(proof) % 32 == 0)

        rhs_leaf = self.wallet.create_rhs_leaf(token_id)
        # Initialize computed_hash to leaf
        computed_hash = self.wallet.create_leaf(self.wallet.public_key, rhs_leaf)

        idx = token_id

        for i in range(0, len(proof), 32):
            el = proof[i : i + 32]

            if idx % 2 == 0:
                computed_hash = self.wallet.hash_padded(computed_hash, el)
            else:
                computed_hash = self.wallet.hash_padded(el, computed_hash)

            idx = idx // 2

        return jsonify(
            valid=computed_hash == root
        )
