import ed_baby_jubjub.ed25519 as ed
import hashlib
import random

class Wallet(object):
    def __init__(self, wallet_file='wallet_file'):
        self.wallet_file = wallet_file
        self.secret_key = None
        self.public_key = None

        try:
            self.load_key_pair()

            print('Loaded existing key pair')
        except Exception as e:
            self.gen_key_pair()

            print('Generated new key pair')

        print('Public Key: {}'.format(self.public_key))

    def sign(self, msg):
        return ed.signature(msg, self.secret_key, self.public_key) 

    def gen_key_pair(self):
        sk = self.gen_salt(64)
        pk = ed.publickey(sk)

        self.secret_key = sk
        self.public_key = pk

        with open(self.wallet_file, "w+") as f:
            f.write(self.secret_key)

    def load_key_pair(self):
        f = open(self.wallet_file, "r")
        data = f.read()

        sk = data
        pk = ed.publickey(sk)

        self.secret_key = sk
        self.public_key = pk

    def gen_salt(self, i):
        salt = [random.choice("0123456789abcdef") for x in range(0, i)]
        return "".join(salt)

    def create_rhs_leaf(self, token_id):
        return self.hash_padded(hex(token_id)[2] * 64, "1" * 64)[2:]

    def create_leaf(self, pub_key, msg):
        pk = ed.encodepoint(pub_key)
        leaf = self.hash_padded(pk, msg)

        return leaf[2:]

    def hash_padded(self, left, right):
        x1 = int(left , 16).to_bytes(32, "big")
        x2 = int(right , 16).to_bytes(32, "big") 
        data = x1 + x2
        answer = hashlib.sha256(data).hexdigest()
        return "0x" + answer


