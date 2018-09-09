import { REQUEST_TRANSFER_TOKEN } from "../constants/action-types";

const tokenReducer = (state = [], action) => {
  switch (action.type) {
    case REQUEST_TRANSFER_TOKEN:
      return [...state, action.payload];
    default:
      return state;
  }
};

export default tokenReducer;
