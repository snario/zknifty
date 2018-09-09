import { REQUEST_TRANSFER_TOKEN, RECEIVE_MY_TOKENS, RECEIVE_MERKLE_PROOF } from "../constants/action-types";

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
      return action.tokens.map(x => ({...x, verified: false}));
    case REQUEST_TRANSFER_TOKEN:
      return [...state, action.payload];
    case RECEIVE_MERKLE_PROOF:
      console.log('Verified merkle proof')
      console.log('state is ', state)
      let received_uid = action.uid.uid
      for(let i = 0 ; i< state.length; i++) {
          if (state[i].uid == parseInt(received_uid)) {
              state[i].verified = true
          }
      }
      console.log('updated state', state)
      // TODO: figure out if actually true
      // data type is { "${uid}": ${proof} }
      return state;
    default:
      return state;
  }
};

export default tokenReducer;
