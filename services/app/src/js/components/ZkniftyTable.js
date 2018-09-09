import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import ethers from "ethers";

import { fetchMerkleRoot } from "../actions";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: () => dispatch(fetchMerkleRoot())
  };
};

const mapStateToProps = state => {
  return { merkleRoot: state.merkleRoot };
};

const provider = new ethers
  .providers
  .JsonRpcProvider(process.env.ETHEREUM_JSONRPC_URL);

class ConnectedMerkleRoot extends Component {

  constructor() {
    super();

    this.state = {
      blockNumber: "Loading ...",
    };

    provider.on('block', this.handleBlockMined.bind(this));

    setInterval(function f () {
      provider.send("evm_mine");
      return f;
    }(), 5000);

  }

  handleBlockMined(blockNumber) {
    this.setState({blockNumber});
  }

  componentDidMount() {
    this.props.fetchMerkleRoot();
  }

  render() {
    const { blockNumber } = this.state;

    return (
      <table className="table">
        <tbody>
          <tr>
            <td>Block Number</td>
            <td>{ blockNumber }</td>
          </tr>
          <tr>
            <td>Merkle Root</td>
            <td>{ this.props.merkleRoot }</td>
          </tr>
          <tr>
            <td>Token A Owner</td>
            <td>8ac254767001f13d0db03af324422b55804412fcfcd8147f05c5a73c650971ba</td>
          </tr>
          <tr>
            <td>Token B Owner</td>
            <td>8ac254767001f13d0db03af324422b55804412fcfcd8147f05c5a73c650971ba</td>
          </tr>
          <tr>
            <td>Token C Owner</td>
            <td>8ac254767001f13d0db03af324422b55804412fcfcd8147f05c5a73c650971ba</td>
          </tr>
          <tr>
            <td>Token D Owner</td>
            <td>8ac254767001f13d0db03af324422b55804412fcfcd8147f05c5a73c650971ba</td>
          </tr>
        </tbody>
      </table>
    );
  }
}

const MerkleRoot = connect(mapStateToProps, mapDispatchToProps)(ConnectedMerkleRoot);

ConnectedMerkleRoot.propTypes = {
  fetchMerkleRoot: PropTypes.func.isRequired
};

export default MerkleRoot;