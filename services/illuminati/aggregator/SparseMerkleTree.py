from collections import OrderedDict
import hashlib

class SparseMerkleTree(object):
    def __init__(self, depth=64, leaves={}):
        self.depth = depth
        if len(leaves) > 2 ** depth:
            raise self.TreeSizeExceededException(
                'tree with depth {} cannot have {} leaves'.format(
                    depth, len(leaves)
                )
            )

        # Sort the transaction dict by index.
        self.leaves = OrderedDict(sorted(leaves.items(), key=lambda t: t[0]))
        self.default_nodes = self.create_default_nodes(self.depth)
        if leaves:
            self.tree = self.create_tree(
                self.leaves, self.depth, self.default_nodes
            )
            self.root = self.tree[-1][0]
        else:
            self.tree = []
            self.root = self.default_nodes[self.depth]

    def create_default_nodes(self, depth):
        # Default nodes are the nodes whose children are both empty nodes at
        # each level.
        default_leaf = '0x' + '0' * 64
        default_nodes = [default_leaf]
        for level in range(1, depth + 1):
            prev_default = default_nodes[level - 1]
            default_nodes.append(self.hashPadded(prev_default, prev_default))
        return default_nodes

    def create_tree(self, ordered_leaves, depth, default_nodes):
        tree = [ordered_leaves]
        tree_level = ordered_leaves
        for level in range(depth):
            next_level = {}
            for index, value in tree_level.items():
                if index % 2 == 0:
                    co_index = index + 1
                    if co_index in tree_level:
                        next_level[index // 2] = self.hashPadded(
                            value, tree_level[co_index]
                        )
                    else:
                        next_level[index // 2] = self.hashPadded(
                            value, default_nodes[level]
                        )
                else:
                    # If the node is a right node, check if its left sibling is
                    # a default node.
                    co_index = index - 1
                    if co_index not in tree_level:
                        next_level[index // 2] = self.hashPadded(
                            default_nodes[level], value
                        )
            tree_level = next_level
            tree.append(tree_level)
        return tree

    def create_merkle_proof(self, uid):
        # Generate a merkle proof for a leaf with provided index.
        # First `depth/8` bytes of the proof are necessary for checking if
        # we are at a default-node
        index = uid
        proof = b''

        # Edge case of tree being empty
        if len(self.tree) == 0:
            return b'\x00\x00\x00\x00\x00\x00\x00\x00'

        for level in range(self.depth):
            sibling_index = index + 1 if index % 2 == 0 else index - 1
            index = index // 2
            if sibling_index in self.tree[level]:
                proof += self.tree[level][sibling_index]

        return proof

    def verify(self, uid, proof):
        ''' Checks if the proof for the leaf at `uid` is valid'''
        # assert (len(proof) -8 % 32) == 0
        assert len(proof) <= 2056

        index = uid
        p = 0
        if index in self.leaves:
            computed_hash = self.leaves[index]
        # in case the tx is not included, computed_hash is the default leaf
        else:
            computed_hash = self.default_nodes[-1]

        for d in range(self.depth):
            proof_element = proof[p : p + 32]
            p += 32
            if index % 2 == 0:
                computed_hash = self.hashPadded(computed_hash, proof_element)
            else:
                computed_hash = self.hashPadded(proof_element, computed_hash)
            index = index // 2
        return computed_hash == self.root

    def hashPadded(self, left, right):
        x1 = int(left, 16).to_bytes(32, "big")
        x2 = int(right, 16).to_bytes(32, "big")
        data = x1 + x2
        answer = hashlib.sha256(data).hexdigest()
        return "0x" + answer

    class TreeSizeExceededException(Exception):
        """there are too many leaves for the tree to build"""

