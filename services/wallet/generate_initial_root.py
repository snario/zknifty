from wallet import Wallet
from SparseMerkleTree import SparseMerkleTree

# Generates a merkle root that will be used by the Verifier contract to seed
# the original owner of the coins

import os

bob_sk = os.getenv('BOB_SK')
alice_sk = os.getenv('ALICE_SK')

bobWallet = Wallet(sk= bob_sk)
aliceWallet = Wallet(sk= alice_sk)

# tokens = [ w.create_rhs_leaf(i) for i in range(4) ]
leaves = {}

# token 0 & 1 to Bob
leaves[0] = bobWallet.create_leaf(bobWallet.public_key, str(0))
leaves[1] = bobWallet.create_leaf(bobWallet.public_key, str(1))

# token 2 & 3 to Alice
leaves[2] = aliceWallet.create_leaf(aliceWallet.public_key, str(2))
leaves[3] = aliceWallet.create_leaf(aliceWallet.public_key, str(3))

print(leaves)
tree = SparseMerkleTree(2, leaves)
print (f"The root for the initialization of the contract is {tree.root}")
