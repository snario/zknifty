import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import { fetchMerkleRoot } from "../actions/index";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: article => dispatch(fetchMerkleRoot(article))
  };
};

class ConnectedMerkleRoot extends Component {

  constructor() {
    super();

    this.state = {
      merkleRoot: "Loading ..."
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async handleSubmit() {
    const hash = await this.props.fetchMerkleRoot(42);
    this.setState({ merkleRoot: "TODO: get merkle root" });
  }

  componentDidMount() {
      this.handleSubmit();
  }

  render() {
    const { merkleRoot } = this.state;

    return (
      <div>
        <h2> { merkleRoot }</h2>
        <button
            type="submit"
            className="btn btn-success btn-lg"
            onClick={ this.handleSubmit }
        >
          Refresh
        </button>
      </div>
    );
  }
}

const MerkleRoot = connect(null, mapDispatchToProps)(ConnectedMerkleRoot);

ConnectedMerkleRoot.propTypes = {
  fetchMerkleRoot: PropTypes.func.isRequired
};

export default MerkleRoot;
