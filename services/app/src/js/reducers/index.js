import { combineReducers } from "redux";
import tokenReducer from "./tokenReducer";
import merkleReducer from "./merkleReducer";

export default combineReducers({
    merkleRoot: merkleReducer,
    tokens: tokenReducer
});
