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

sys.path.insert(0, '../depends/roll_up/pythonWrapper')
sys.path.insert(0, 'prover')
sys.path.insert(0, 'signer')

from wallet import Wallet
from prover import *

from constants import *
from classes import *

from utils import *

nWallets = 4

if __name__ == "__main__":

    old_leaf = []
    new_leaf = []

    # Wallet array
    wallets = []
    txs = []

    for i in range(nWallets):
        wallets.append(Wallet())

    # Iterate over transactions
    for j in range(nWallets-1):

        # New wallet
        wallet = wallets[j]
        
        # The old leaf is previous pubkey + previous message
        old_leaf.append(createLeaf(wallet.public_key, rhs_leaf))
        
        # The new leaf is current pubkey with current message
        new_leaf.append(createLeaf(wallets[j+1].public_key, rhs_leaf))
        
        # The message to sign is the previous leaf with the new leaf
        message = hashPadded(old_leaf[j], new_leaf[j])
        
        # Remove '0x' from byte
        message = message[2:]

        # Obtain Signature 
        r,s = wallet.sign(message)

        # Tx object
        txs.append(SignedTransferTransaction(wallet.public_key, wallet.secret_key, 1, r, s))

        console.log(tx)
    
    # # Get zk proof and merkle root
    genWitness(leaves, pub_x, pub_y, address, tree_depth, 
                                 rhs_leaf, new_leaf , R_x, R_y, S)              

    # proof["a"] = hex2int(proof["a"])
    # proof["a_p"] = hex2int(proof["a_p"])
    # proof["b"] = [hex2int(proof["b"][0]), hex2int(proof["b"][1])]
    # proof["b_p"] = hex2int(proof["b_p"])
    # proof["c"] = hex2int(proof["c"])
    # proof["c_p"] = hex2int(proof["c_p"])
    # proof["h"] = hex2int(proof["h"])
    # proof["k"] = hex2int(proof["k"])
    # proof["input"] = hex2int(proof["input"]) 

    # #root , merkle_tree = utils.genMerkelTree(tree_depth, leaves[0])
    # try:

    # except:

    #     raise

