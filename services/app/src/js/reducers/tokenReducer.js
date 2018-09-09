import { REQUEST_TRANSFER_TOKEN, RECEIVE_MY_TOKENS } from "../constants/action-types";

// const STARTING_BALANCES = [
//   {
//     name: "Bob",
//     address: process.env.BOB_PK,
//     merkleProof: {
//       proof: 0xa,
//       timestamp: 2
//     },
//     confidence: process.env.BOB_PK,
//   }
// ];

const tokenReducer = (state = [], action) => {
  switch (action.type) {
    case RECEIVE_MY_TOKENS:
      return action.tokens;
    case REQUEST_TRANSFER_TOKEN:
      return [...state, action.payload];
    default:
      return state;
  }
};

export default tokenReducer;
