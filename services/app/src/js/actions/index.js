import fetch from "cross-fetch";
import ethers from "ethers";

export const requestTransferToken = transferDetails => ({
  type: "REQUEST_TRANSFER_TOKEN",
  payload: transferDetails
});

export const requestMerkleRoot = () => ({
  type: "REQUEST_MERKLE_ROOT"
});

export const receiveMerkleRoot = (merkleRoot) => ({
  type: "RECEIVE_MERKLE_ROOT",
  merkleRoot
});

export const fetchMerkleRoot = () => {
  // TODO: Should we use the fetch library instead of ethers?
  // TODO: Error handling for blockchain not responding 
  // TODO: Don't use ABI, use ethers.js string interface
  return dispatch => {
    dispatch(requestMerkleRoot());
    return new ethers
      .Contract(
        process.env.MIXIMUS_ADDR,
        require("./roll_up.json").abi,
        new ethers.providers.JsonRpcProvider(process.env.ETHEREUM_JSONRPC_URL)
      )
      .functions
      .getRoot()
      .then(merkleRoot => dispatch(receiveMerkleRoot(merkleRoot)));
  };
};
