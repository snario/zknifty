import sys
sys.path.insert(0, "../../depends/roll_up/pythonWrapper")
sys.path.insert(0, "../")

from wallet import Wallet
from constants import rhs_leaf
from .web_service import WebService

class Client(object):
    def __init__(self, wallet, web_service):
        self.wallet = wallet
        self.web_service = web_service

    def transfer(self, receiver_pub_key, token_id):
        msg = self.create_tx(receiver_pub_key)
        R, S = self.wallet.sign(msg)
        end_point = '/send_tx'
        response = self.web_service.request(end_point, 'POST')
        return response.text

    def create_tx(self, receiver_pub_key):
        old_leaf = self.wallet.create_leaf(self.wallet.public_key, rhs_leaf)
        new_leaf = self.wallet.create_leaf(receiver_pub_key, rhs_leaf)
        return self.wallet.hash_padded(old_leaf, new_leaf)[2:]

    def get_proof(self, token_id):
        end_point = '/proof/{}'.format(token_id)
        response = self.web_service.request(end_point, 'GET')
        return response.text

    def get_tokens(self):
        pass
