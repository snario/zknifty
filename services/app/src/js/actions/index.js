import fetch from "cross-fetch";
import ethers from "ethers";

export const requestTransferToken = transferDetails => ({
  type: "REQUEST_TRANSFER_TOKEN",
  payload: transferDetails
});

export const receiveTransferToken = () => ({
  type: "RECEIVE_TRANSFER_TOKEN_ACK"
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

export const sendToken = (receiverPubKey, uid) => {
  return dispatch => {
    return fetch(`http://localhost:5001/sign_transfer`, {
      method: "POST",
      body: JSON.stringify({
        "receiver_pub_key": receiverPubKey,
        "token_id": uid
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(
      response => response.json(),
      error => console.log("❌ An error occurred.", error)
    )
    .then(
      json => {
        const toX = json.receiver_pub_key[0]
        const toY = json.receiver_pub_key[1]
        const uid = json.token_id
        const sig = json.sig[0][0].toString(16) + json.sig[0][1].toString(16) + json.sig[1].toString(16)
        return fetch(`${process.env.ILLUMINATI_URL}/send_tx`, {
          method: "POST",
          body: new URLSearchParams({
            to_x: toX,
            to_y: toY,
            uid: uid,
            sig: sig
          }),
          headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
          }
        })
      }
    )
    .then(
      response => response.json(),
      error => console.log("❌ An error occurred.", error)
    )
    .then(json => dispatch(receiveTransferToken()))
  };
};

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