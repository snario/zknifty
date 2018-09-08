'''   
    copyright 2018 to the roll_up Authors

    This file is part of roll_up.

    roll_up is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    roll_up is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with roll_up.  If not, see <https://www.gnu.org/licenses/>.
'''


import sys
sys.path.insert(0, '../../depends/roll_up/pythonWrapper')
sys.path.insert(0, "../../depends/roll_up/depends/baby_jubjub_ecc/tests")

sys.path.insert(0, '../../depends/roll_up/contracts')
from contract_deploy import contract_deploy, verify, hex2int

from 
from helper import *
from classes import * 
from utils import getSignature, createLeaf, hashPadded, libsnark2python
import ed25519 as ed

from web3 import Web3, HTTPProvider, TestRPCProvider

host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
w3 = Web3(HTTPProvider(f"http://{host}:8545"));

# Place to store prover and verifier keys
pk_output = "../zksnark_element/pk.raw"  # Prover key
vk_output = "../zksnark_element/vk.json" # Verifier key

def GenerateMassTransferProof(signedTransferTransactions):

    pub_x = []
    pub_y = []
    leaves = []
    R_x = []
    R_y = []
    S = []
    previous_owners = []
    new_owners = []
    address = []
    public_key = []

    # Public key of sender from first tx
    public_key.append(tx.senderPubKey)

    # Iterate over transactions
    for j in range(1,len(signedTransferTransactions)+1):

        leaves.append([])

        # Current transaction object
        tx = signedTransferTransactions[j-1]

        # Append sender pubkey
        public_key.append(tx.senderPubKey)
        
        # The old owner is previous pubkey + RHS
        previous_owners.append(createLeaf(tx.senderPubKey, rhs_leaf))
        
        # The new leaf is current pubkey with RHS
        new_owners.append(createLeaf(tx.receiverPubKey, rhs_leaf))
        
        # The message to sign is the previous leaf with the new leaf
        message = hashPadded(previous_owners[j-1], new_owners[j-1])
        
        # Remove '0x' from byte
        message = message[2:]

        # Check the signer is correct
        ed.checkvalid(tx.R, tx.S, message, tx.senderPubKey)

        # Now we reverse the puplic key by bit
        # we have to reverse the bits so that the 
        # unpacker in libsnark will return us the 
        # correct field element
        # To put into little-endian
        pub_key_x = hex(int(''.join(str(e) for e in hexToBinary(hex(public_key[j-1][0]))[::-1]),2)) 
        pub_key_y = hex(int(''.join(str(e) for e in hexToBinary(hex(public_key[j-1][1]))[::-1]),2))
           
        tx.R[0] = hex(int(''.join(str(e) for e in hexToBinary(hex(tx.R[0]))[::-1]),2))
        tx.R[1] = hex(int(''.join(str(e) for e in hexToBinary(hex(tx.R[1]))[::-1]),2))
        
        # Two r on x and y axis of curve
        R_x.append(tx.R[0])
        R_y.append(tx.R[1])
        
        # Store s
        S.append(s)
        
        # Store public key
        pub_x.append(pub_key_x) 
        pub_y.append(pub_key_y)
        
        # 
        leaves[j-1].append(previous_owners[j-1])

        #
        address.append(0)

    # Get zk proof and Merkle root
    proof, root = generateWitness(leaves, pub_x, pub_y, address, tree_depth, 
                                  rhs_leaf, new_owners , R_x, R_y, S) 

    #Build proof for contract
    proof["a"] = hex2int(proof["a"])
    proof["a_p"] = hex2int(proof["a_p"])
    proof["b"] = [hex2int(proof["b"][0]), hex2int(proof["b"][1])]
    proof["b_p"] = hex2int(proof["b_p"])
    proof["c"] = hex2int(proof["c"])
    proof["c_p"] = hex2int(proof["c_p"])
    proof["h"] = hex2int(proof["h"])
    proof["k"] = hex2int(proof["k"])
    proof["input"] = hex2int(proof["input"]) 


##
# @dev:
#    Generate the witness
#
# @params:
#   leaves:
#   public_key_x:
#   public_key_y:
#   address:
#   tree_depth:
#   _rhs_leaf:
#   _new_owners:
#   r_x:
#   r_y:
#   s:
#
# @returns:
#   Proof Object
#
##
def generateWitness(leaves, public_key_x, public_key_y, address, tree_depth, _rhs_leaf, _new_owners, r_x, r_y, s):

    #
    path = []
    address_bits = []
    pub_key_x = []
    pub_key_y = [] 
    roots = []
    paths = []

    #
    previous_owners = [] 
    new_owners = []
    r_x_bin_array = []
    r_y_bin_array = []
    s_bin_array = []

    #Number of transactions
    noTx = len(leaves)

    for i in range(noTx): 

        root , merkle_tree = utils.genMerkelTree(tree_depth, leaves[i])
        path , address_bit = utils.getMerkelProof(leaves[i], address[i], tree_depth)

        path = [binary2ctypes(hexToBinary(x)) for x in path] 

        address_bit = address_bit[::-1]
        path = path[::-1]
        paths.append(((c.c_bool*256)*(tree_depth))(*path))

        pub_key_x.append(binary2ctypes(hexToBinary(public_key_x[i])))
        pub_key_y.append(binary2ctypes(hexToBinary(public_key_y[i])))

        roots.append(binary2ctypes(hexToBinary(root)))

        address_bits.append((c.c_bool*tree_depth)(*address_bit))

        previous_owners.append(binary2ctypes(hexToBinary(_rhs_leaf[i])))
        new_owners.append(binary2ctypes(hexToBinary(_new_owners[i])))

        r_x_bin_array.append(binary2ctypes(hexToBinary(r_x[i])))
        r_y_bin_array.append(binary2ctypes(hexToBinary(r_y[i])))
        s_bin_array.append(binary2ctypes(hexToBinary(hex(s[i]))))

    pub_key_x_array = ((c.c_bool*256)*(noTx))(*pub_key_x)
    pub_key_y_array = ((c.c_bool*256)*(noTx))(*pub_key_y)
    merkle_roots = ((c.c_bool*256)*(noTx))(*roots)
    previous_owners = ((c.c_bool*256)*(noTx))(*previous_owners)
    new_owners = ((c.c_bool*256)*(noTx))(*new_owners)
    r_x_bin = ((c.c_bool*256)*(noTx))(*r_x_bin_array)
    r_y_bin = ((c.c_bool*256)*(noTx))(*r_y_bin_array)
    s_bin = ((c.c_bool*256)*(noTx))(*s_bin_array)
    paths = ((c.c_bool*256)*(tree_depth) * noTx)(*paths)
    address_bits = ((c.c_bool)*(tree_depth) * noTx)(*address_bits)

    proof = prove(paths, pub_key_x_array, pub_key_y_array, merkle_roots,  address_bits, previous_owners, new_owners, r_x_bin, r_y_bin, s_bin, tree_depth, noTx)

    proof = json.loads(proof.decode("utf-8"))
    root , merkle_tree = utils.genMerkelTree(tree_depth, leaves[0])

    return(proof, root)

   
