import thunkMiddleware from 'redux-thunk'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import { createStore, applyMiddleware, compose } from 'redux'
import rootReducer from "../reducers/index";

const persistConfig = {
  key: 'root',
  storage,
}

const persistedReducer = persistReducer(persistConfig, rootReducer)

export default () => {
  let store = createStore(
    persistedReducer,
    compose(
      applyMiddleware(thunkMiddleware),
      // window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
    )
  );
  let persistor = persistStore(store)
  return { store, persistor }
}
