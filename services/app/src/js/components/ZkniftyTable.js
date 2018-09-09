import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import ethers from "ethers";

import { fetchMerkleRoot } from "../actions";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: article => dispatch(fetchMerkleRoot(article))
  };
};

const provider = new ethers
  .providers
  .JsonRpcProvider(process.env.ETHEREUM_JSONRPC_URL);

class ConnectedMerkleRoot extends Component {

  constructor() {
    super();

    this.state = {
      merkleRoot: "Loading ...",
      blockNumber: "Loading ...",
    };

    this.handleSubmit = this.handleSubmit.bind(this);

    provider.on('block', this.handleBlockMined.bind(this));

    setInterval(() => provider.send("evm_mine"), 5000);
  }

  handleBlockMined(blockNumber) {
    this.setState({blockNumber});
  }

  async handleSubmit() {
    const hash = await this.props.fetchMerkleRoot(42);
    this.setState({ merkleRoot: "TODO: get merkle root" });
  }

  componentDidMount() {
    this.handleSubmit();
  }

  render() {
    const { merkleRoot, blockNumber } = this.state;

    return (
      <table className="table">
        <tbody>
          <tr>
            <td>Block Number</td>
            <td>{ blockNumber }</td>
          </tr>
          <tr>
            <td>Merkle Root</td>
            <td>{ merkleRoot }</td>
          </tr>
          <tr>
            <td>Token A Owner</td>
            <td>{ merkleRoot }</td>
          </tr>
          <tr>
            <td>Token B Owner</td>
            <td>{ merkleRoot }</td>
          </tr>
        </tbody>
      </table>
    );
  }
}

const MerkleRoot = connect(null, mapDispatchToProps)(ConnectedMerkleRoot);

ConnectedMerkleRoot.propTypes = {
  fetchMerkleRoot: PropTypes.func.isRequired
};

export default MerkleRoot;