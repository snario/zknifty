import sys
# Add path to baby_jubjub_ecc dependency for ed25519 with baby_jubjub curve
sys.path.insert(0, '../../depends/roll_up/depends/baby_jubjub_ecc/tests')

import ed25519 as ed
from exceptions import WalletException
import random

class Wallet(object):
    def __init__(self, wallet_file='wallet_file'):
        self.wallet_file = wallet_file
        self.secret_key = None
        self.public_key = None

        self.gen_key_pair()

    def sign(self, msg):
        return ed.signature(msg, self.secret_key, self.public_key) 

    def gen_key_pair(self):
        sk = self.gen_salt(64)
        pk = ed.publickey(sk)

        self.secret_key = sk
        self.public_key = pk

    def gen_salt(self, i):
        salt = [random.choice("0123456789abcdef") for x in range(0, i)]
        return "".join(salt)

