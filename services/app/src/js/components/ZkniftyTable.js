import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import ethers from "ethers";

import { sendToken, fetchMerkleRoot, fetchMyTokens, fetchMerkleProof } from "../actions";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: () => dispatch(fetchMerkleRoot()),
    fetchMyTokens: () => dispatch(fetchMyTokens()),
    fetchMerkleProof: (uid) => dispatch(fetchMerkleProof(uid)),
    sendToken: (receiverPubKey, uid) => dispatch(sendToken(receiverPubKey, uid))
  };
};

const mapStateToProps = state => {
  return {
    tokens: state.tokens,
    merkleRoot: state.merkleRoot
  };
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
    this.props.fetchMyTokens();
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
          {
            this.props.tokens.map(el => (
              <tr key={ el.uid }>
                <td>{ el.uid }</td>
                <td>
                  { el.title }
                  <button
                    className="btn btn-link"
                    onClick={ () => this.props.fetchMerkleProof(el.uid) }>
                    Verify
                  </button>
                  <button
                    className="btn btn-link"
                    onClick={ () => this.props.sendToken([process.env.ALICE_PK_X, process.env.ALICE_PK_Y], el.uid) }>
                    Private Send
                  </button>
                </td>
              </tr>
            ))
          }
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