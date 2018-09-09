# Aggregator class that will submit things
import rpyc
import sys
import os
from os import path

from .exceptions import TransactionAlreadyIncludedException

from .SparseMerkleTree import SparseMerkleTree

# TODO: Recover owner from signatures instead
#       of assuming it's valid

class Aggregator(object):
    def __init__(self, authority, verifier): # init_balances is a dictionary of balances per user
        # self.proof_service_conn = rpyc.connect("proof_service", 18861)
        alice = [ int(os.environ['ALICE_PK_X']), int(os.environ['ALICE_PK_Y']) ]
        bob = [ int(os.environ['BOB_PK_X']), int(os.environ['BOB_PK_Y']) ]
        coin_owners = { 0: alice, 1: alice, 2: bob, 3: bob}
        self.verifier = verifier
        self.authority = authority
        self.coin_owners = coin_owners
        self.tree_depth = 2
        self.pending_transactions = {} # pending_transactions that get reset
                                       # after each commitment

    # sender / to are both arrays
    def send_transaction(self, uid, to, sig):
        """
            Sends coin to `to` and updates the state
        """
        # Prevent dup txs
        if uid in self.pending_transactions.keys():
            raise TransactionAlreadyIncludedException('duplicate tx')

        # owner = edrecover(msg, sig)
        # assert owner == self.coin_owners[uid]
        msg =f"Sent coin {uid} to {to}"
        self.coin_owners[uid] = to
        self.pending_transactions[uid] = {
                # 'sender': sender,
                'to': to,
                'sig': sig
                }
        print(msg)
        return msg

    def get_owner(self, uid):
        try:
            return self.coin_owners[uid]
        except:
            return "Coin not found"

    def get_coins(self, owner):
        # owner = edrecover(msg, sig) 
        # print(owner)
        # print(self.coin_owners)
        filtered_coins = { 
                key : value 
                for key, value in self.coin_owners.items() if
                value == owner
        }
        return filtered_coins

    def get_proof(self, uid):
        """
            Should return merkle proof of ownership for `uid`
        """
        try:
            tree = SparseMerkleTree(self.tree_depth, self.coin_owners)
            return tree.create_merkle_proof(uid)
        except:
            return "Could not retrieve proof"

    def prove(self, txs):
        """
            prove.py stuff for generating 
            the proof for the current state
            fetch the proof from the rpyc service
        """
        try:
            proof = self.proof_service_conn.root.proof(txs)
            return proof
        except:
            return "Could not generate proof"
    
    def submit_state(self):
        # Generate the proof for the current 
        try: 
            root = self.prove(self.pending_transactions)
            self.verifier.functions.submitState(root)
            # Reset the pending txs
            self.pending_transactions = {}
        except:
            return "Could not submit state"
