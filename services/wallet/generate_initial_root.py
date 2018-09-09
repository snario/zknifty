from wallet import Wallet
from SparseMerkleTree import SparseMerkleTree

# Generates a merkle root that will be used by the Verifier contract to seed
# the original owner of the coins

import os

bob_pk_x = os.getenv('BOB_PK_X')
bob_pk_y = os.getenv('BOB_PK_Y')

alice_pk_x = os.getenv('ALICE_PK_X')
alice_pk_y = os.getenv('ALICE_PK_Y')

# tokens = [ w.create_rhs_leaf(i) for i in range(4) ]
leaves = {}

# token 0 & 1 to Bob
leaves[0] = w.create_leaf([bob_pk_x, bob_pk_y], str(0))
leaves[1] = w.create_leaf([bob_pk_x, bob_pk_y], str(1))

# token 2 & 3 to Alice
leaves[2] = w.create_leaf([alice_pk_x, alice_pk_y], str(2))
leaves[3] = w.create_leaf([alice_pk_x, alice_pk_y], str(3))


print(leaves)
tree = SparseMerkleTree(2, leaves)
print (f"The root for the initialization of the contract is {tree.root}")
