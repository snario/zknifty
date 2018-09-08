# Aggregator class that will submit things

class Aggregator(object):
    def __init__(self, authority, verifier):
        self.verifier = verifier
        self.authority = authority
        self.coin_owners = {}

    def send_transaction(self, uid, to, sig):
        """
            Sends coin to `to` and updates the state    
        """
        txHash = "0x0"
        print(f'Sent coin {uid} to {to}')
        assert True # check that `sig` matches the owner's pk
        self.coin_owners[uid] = to
        return txHash
    
    def get_owner(self, uid):
        return self.coin_owners[uid]

    def get_proof(self, uid):
        """ 
            Should return merkle proof of inclusion for `uid`
        """
        return '0'

    def prove(self):
        """
            prove.py stuff for generating 
            the proof for the current state
        """
        return '0' * 32 

    def submit_state(self):
        root = self.prove()
        self.verifier.functions.submitState(root)
