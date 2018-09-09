import React from "react";
import { PersistGate } from 'redux-persist/integration/react'
import { render } from "react-dom";
import { Provider } from "react-redux";
import Store from "./store/index";
import App from "./components/App";

const { store, persistor } = Store();

render(
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <App />
    </PersistGate>
  </Provider>,
  document.getElementById("app")
);
