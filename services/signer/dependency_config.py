from signer.client import Client
from signer.web_service import WebService
from wallet import Wallet

class DependencyContainer(object):
    def __init__(self):
        self._signer = None

    def get_signer(self):
        if self._signer is None:
            wallet = Wallet()
            web_service = WebService('http://localhost:8546')
            self._signer = Client(wallet, web_service)
        return self._signer

container = DependencyContainer()