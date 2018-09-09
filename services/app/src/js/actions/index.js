import fetch from "cross-fetch";

export const requestTransferToken = transferDetails => ({
  type: "REQUEST_TRANSFER_TOKEN",
  payload: transferDetails
});

export const requestMerkleRoot = () => ({
  type: "REQUEST_MERKLE_ROOT"
});

export const receiveMerkleRoot = (json) => ({
  type: "REQUEST_MERKLE_ROOT",
  data: json
});

export const fetchMerkleRoot = identityProof => {
  return dispatch => {
    dispatch(requestMerkleRoot());
    return fetch(`${process.env.ILLUMINATI_URL}/proof/${identityProof}`)
      .then(
        response => response.json(),
        error => console.log("❌ An error occurred.", error)
      )
      .then(json => dispatch(receiveMerkleRoot(json)));
  };
};
