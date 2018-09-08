import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

const mapStateToProps = state => {
  return { tokens: state.tokens };
};

const ConnectedList = ({ tokens }) => (
  <ul className="list-group list-group-flush">
    {tokens.map(el => (
      <li className="list-group-item" key={el.id}>
        {el.title}
      </li>
    ))}
  </ul>
);

const List = connect(mapStateToProps)(ConnectedList);

ConnectedList.propTypes = {
  tokens: PropTypes.array.isRequired
};

export default List;
