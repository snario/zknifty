import { RECEIVE_MERKLE_ROOT } from "../constants/action-types";

const merkleReducer = (state = "", action) => {
  switch (action.type) {
    case RECEIVE_MERKLE_ROOT:
      return action.merkleRoot;
    default:
      return state;
  }
};

export default merkleReducer;
