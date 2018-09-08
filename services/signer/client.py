from .wallet import Wallet
from .web_service import WebService
from ..classes import SignedTransferTransaction

class Client(object):
    def __init__(self, wallet, web_service):
        self.wallet = wallet
        self.web_service = web_service

    def transfer(self, receiver_pub_key, token_id):
        pass
