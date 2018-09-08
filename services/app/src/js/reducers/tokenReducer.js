import { TRANSFER_TOKEN } from "../constants/action-types";

const START_TOKENS = [
  {title: 1, id: 1},
  {title: 2, id: 2},
  {title: 3, id: 3},
  {title: 4, id: 4}
]

const tokenReducer = (state = START_TOKENS, action) => {
  switch (action.type) {
    case TRANSFER_TOKEN:
      return [...state, action.payload];
    default:
      return state;
  }
};

export default tokenReducer;
