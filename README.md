<div align="center">
    <img src="./assets/logo.svg" height="80px" /> 
    <p><b>zknifty</b>: Zero-knowledge transactions of non-fungible tokens on Ethereum </p>
</div>

zknifty is an experiment in using an implementation of zero-knowledge merkle tree proofs to facilitate bulk transactions of non-fungible tokens on Ethereum. It was built as a hack at [ETHBerlin](https://ethberlin.com). This work was **strongly** inspired and influenced by https://github.com/barryWhiteHat/roll_up.

# How it works
Merkle trees can lead to significant data compression for smart contracts, where an entire contract state can be compressed in a single `bytes32` hash on-chain. In this NFT repository, each leaf of the merkle tree represents the ID of a Non-Fungible Token and each leaf also stores the current owner of the corresponding token. However, since the data composing the merkle-tree is stored off-chain, it is difficult for contracts to validate changes to the merkle tree. Here, we utilize the properties of zk-SNARKs to guarantee that the merkle tree was updated according to verify specific rules. These rules where as follow :

* The actual owner of the token signed a message
* This message is composed of the token ID and the receiver address
* The signature is valid
* The token transfer of ownership is reflected in the new merkle tree

The token contract will accept a new merkle root **only if** all the conditions above are met. Additional conditions are needed to make the contract secure, hence **this contract is not to be used in production**. 


