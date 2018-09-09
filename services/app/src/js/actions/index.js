import fetch from "cross-fetch";
import ethers from "ethers";

export const requestTransferToken = transferDetails => ({
  type: "REQUEST_TRANSFER_TOKEN",
  payload: transferDetails
});

export const requestMyTokens = (address, signature) => ({
  type: "REQUEST_MY_TOKENS",
  address,
  signature
});

export const receiveMyTokens = (tokens) => ({
  type: "RECEIVE_MY_TOKENS",
  tokens
});

export const requestMerkleRoot = () => ({
  type: "REQUEST_MERKLE_ROOT"
});

export const receiveMerkleRoot = (merkleRoot) => ({
  type: "RECEIVE_MERKLE_ROOT",
  merkleRoot
});

export const requestMerkleProof = (uid) => ({
  type: "REQUEST_MERKLE_PROOF",
  uid
});

export const receiveMerkleProof = (uid, merkleProof) => ({
  type: "RECEIVE_MERKLE_PROOF",
  uid,
  merkleProof
});

export const fetchMyTokens = (address, signature) => {
  // TODO: Don't hardcode BOB
  return dispatch => {
    const x = process.env.BOB_PK_X;
    const y = process.env.BOB_PK_Y;
    dispatch(requestMyTokens());
    return fetch(`${process.env.ILLUMINATI_URL}/coins?x=${x}&y=${y}`)
    .then(
      response => response.json(),
      error => console.log("❌ An error occurred.", error)
    )
    .then(json => dispatch(receiveMyTokens(json)));
  };
};

export const fetchMerkleProof = (uid, signature) => {
  return dispatch => {
    dispatch(requestMerkleProof());
    return fetch(`${process.env.ILLUMINATI_URL}/proof/${uid}`)
    .then(
      response => response.json(),
      error => console.log("❌ An error occurred.", error)
    )
    .then(json => dispatch(receiveMerkleProof(json)));
  };
};

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
