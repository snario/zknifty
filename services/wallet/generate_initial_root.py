from wallet import Wallet
from SparseMerkleTree import SparseMerkleTree

w = Wallet()

# Generates a merkle root that will be used by the Verifier contract to seed
# the original owner of the coins

# tokens = [ w.create_rhs_leaf(i) for i in range(4) ]
leaves = {}
for i in range(4):
    leaves[i] = w.create_leaf(w.public_key, str(i))

print(leaves)
tree = SparseMerkleTree(2, leaves)
print (f"The root for the initialization of the contract is {tree.root}")
