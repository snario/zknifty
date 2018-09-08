from aggregator.aggregator import Aggregator
from aggregator.aggregator_client import AggregatorClient


class DependencyContainer(object):
    def __init__(self):
        self._roll_up = None
        self._aggregator = None
        self._aggregator_client = None

    def get_aggregator(self):
        if self._aggregator is None:
            authority = '0x0'  # authority pk
            prover = self.get_prover()
            self._aggregator = Aggregator(authority, prover)
        return self._aggregator

    def get_aggregator_client(self):
        if self._aggregator_client is None:
            self._aggregator_client = AggregatorClient(
                'http://localhost:8546',
                'ws://localhost:8546'
            )
            return self._aggregator_client

    def get_prover(self):
        if self._roll_up is not None:
            self._roll_up = 'dummy'


container = DependencyContainer()
