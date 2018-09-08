import { TRANSFER_TOKEN } from "../constants/action-types";

const tokenReducer = (state = [], action) => {
  switch (action.type) {
    case TRANSFER_TOKEN:
      return [...state, action.payload];
    default:
      return state;
  }
};

export default tokenReducer;
