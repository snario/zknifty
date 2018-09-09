import os
from signer.client import Client
from signer.web_service import WebService
from wallet import Wallet

class DependencyContainer(object):
    def __init__(self):
        self._signer = None

    def set_identity(self, identity):
        self._identity = identity

    def get_signer(self):
        if self._signer is None:
            wallet = Wallet(sk=self.get_sk())
            web_service = WebService('http://localhost:8546')
            self._signer = Client(wallet, web_service)
        return self._signer

    def get_sk(self):
        if self._identity == 'bob':
            return os.environ.get('BOB_SK')
        elif self._identity == 'alice':
            return os.environ.get('ALICE_SK')
        else:
            return None

container = DependencyContainer()