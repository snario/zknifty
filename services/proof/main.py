import rpyc


class ProofService(rpyc.Service):

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        print('🔋 Connected to proof service!')
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        print('🔌 Disconnected from proof service!')
        pass

    def exposed_proof(self):
        print('🔖 Received request for zksnark proof.')
        return 42


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ProofService, port=18861)
    print("⚡️ Starting rpyc proof service.")
    t.start()