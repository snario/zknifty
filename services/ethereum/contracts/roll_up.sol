/*    
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
*/

pragma solidity ^0.4.24;

import "./Verifier.sol";


contract roll_up {
    bytes32 root;
    Verifier zksnark_verify;

    event Withdraw (address withdrawer); 

    constructor (address _zksnark_verify, bytes32 _root) {
        zksnark_verify = Verifier(_zksnark_verify);
        root = _root;
    }

    function isTrue (
            uint[2] A,
            uint[2] A_p,
            uint[2][2] B,
            uint[2] B_p,
            uint[2] C,
            uint[2] C_p,
            uint[2] H,
            uint[2] K,
            uint[] input
    ) 
        returns (bool) 
    {

        bytes32 _root = padZero(reverse(bytes32(input[0]))); 
        require(_root == padZero(root));
        require(zksnark_verify.verifyTx(
            A, A_p, B, B_p, C, C_p, H, K, input)
        );
        root = padZero(reverse(bytes32(input[2])));
        return true;
    }

    function getRoot() view returns(bytes32) {
        return root;
    } 

    function padZero(bytes32 x) returns(bytes32) {
        // 0x1111111111111111111111113fdc3192693e28ff6aee95320075e4c26be03308
        return(x & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0);
    }

    function reverseByte(uint a) public pure returns (uint) {
        uint c = 0xf070b030d0509010e060a020c0408000;
        return (( c >> ((a & 0xF)*8)) & 0xF0)   +  
               (( c >> (((a >> 4)&0xF)*8) + 4) & 0xF);
    }

    // flip endianess
    function reverse(bytes32 a) public pure returns(bytes32) {
        uint r;
        uint i;
        uint b;
        for (i = 0; i < 32; i++) {
            b = (uint(a) >> ((31-i)*8)) & 0xff;
            b = reverseByte(b);
            r += b << (i*8);
        }
        return bytes32(r);
    }

}
