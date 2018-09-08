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

sys.path.insert(0, 'prover')
sys.path.insert(0, 'signer')

from wallet import *
from prover import *

if __name__ == "__main__":

    # Wallet array
    wallets = []

    for i in range(3):
        wallets.append(wallet.Wallet())
        print(wallets)
    
    # # Iterate over transactions
    # for j in range (3):


      
    #     # create a random new leaf
    #     # This is just a filler message for test purpose (e.g. 11111111... , 22222211111...)
    #     rhs_leaf.append(hashPadded(hex(j)[2]*64 , "1"*64)[2:])
        
    #     # The old leaf is previous pubkey + previous message
    #     old_leaf.append(createLeaf(public_key[j-1], rhs_leaf[j-1]))
        
    #     # The new leaf is current pubkey with current message
    #     new_leaf.append(createLeaf(public_key[j], rhs_leaf[j]))
        
    #     # The message to sign is the previous leaf with the new leaf
    #     message = hashPadded(old_leaf[j-1], new_leaf[j-1])
        
    #     # Remove '0x' from byte
    #     message = message[2:]
        
    #     # Obtain Signature 
    #     r,s = getSignature(message, sk[j - 1], public_key[j-1])

    #     # check the signauer is correct
    #     ed.checkvalid(r, s, message, public_key[j-1])

    #     # Now we reverse the puplic key by bit
    #     # we have to reverse the bits so that the 
    #     # unpacker in libsnark will return us the 
    #     # correct field element
    #     # To put into little-endian
    #     pub_key_x = hex(int(''.join(str(e) for e in hexToBinary(hex(public_key[j-1][0]))[::-1]),2)) 
    #     pub_key_y = hex(int(''.join(str(e) for e in hexToBinary(hex(public_key[j-1][1]))[::-1]),2))
           
    #     r[0] = hex(int(''.join(str(e) for e in hexToBinary(hex(r[0]))[::-1]),2))
    #     r[1] = hex(int(''.join(str(e) for e in hexToBinary(hex(r[1]))[::-1]),2))
        
    #     # Two r on x and y axis of curve
    #     R_x.append(r[0])
    #     R_y.append(r[1])
        
    #     # Store s
    #     S.append(s)
        
    #     # Store public key
    #     pub_x.append(pub_key_x) 
    #     pub_y.append(pub_key_y)
        
        
    #     leaves[j-1].append(old_leaf[j-1])

    #     address.append(0)
    
    # # Get zk proof and merkle root
    # proof, root = genWitness(leaves, pub_x, pub_y, address, tree_depth, 
    #                             rhs_leaf, new_leaf , R_x, R_y, S)              

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




       


   
