import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import ethers from "ethers";

import {
  sendToken,
  fetchMerkleRoot,
  fetchMyTokens,
  fetchMerkleProof
} from "../actions";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: () => dispatch(fetchMerkleRoot()),
    fetchMyTokens: () => dispatch(fetchMyTokens()),
    fetchMerkleProof: uid => dispatch(fetchMerkleProof(uid)),
    sendToken: (receiverPubKey, uid) => dispatch(sendToken(receiverPubKey, uid))
  };
};

const mapStateToProps = state => {
  return {
    tokens: state.tokens,
    merkleRoot: state.merkleRoot
  };
};

const provider = new ethers.providers.JsonRpcProvider(
  process.env.ETHEREUM_JSONRPC_URL
);

const UI = {
  0: "https://ethglobal.co/img/partners/ethwaterloo.png",
  1: "https://ethglobal.co/img/partners/ethbuenosaires.png",
  2: "https://ethglobal.co/img/partners/ethberlin.png",
  3: "https://ethglobal.co/img/partners/ETHSF.svg"
};

class ConnectedMerkleRoot extends Component {
  constructor() {
    super();

    this.state = {
      blockNumber: "Loading ..."
    };

    provider.on("block", this.handleBlockMined.bind(this));

    setInterval(
      (function f() {
        provider.send("evm_mine");
        return f;
      })(),
      5000
    );
  }

  handleBlockMined(blockNumber) {
    this.setState({ blockNumber });
  }

  componentDidMount() {
    this.props.fetchMerkleRoot();
    this.props.fetchMyTokens();
  }

  render() {
    const { blockNumber } = this.state;

    return (
      <div>
        <section className="mt-5 jumbotron text-center">
          <div className="container">
            <h1 className="jumbotron-heading">
              <code>{this.props.merkleRoot.substr(0, 10)}</code>
            </h1>
            <p className="lead text-muted">
              zknifty is an experiment in using an implementation of
              zero-knowledge merkle tree proofs to facilitate bulk transactions
              of non-fungible tokens on Ethereum.
            </p>
          </div>
        </section>

        <div className="album py-5 bg-light">
          <div className="container">
            <div className="row">
              <div className="col-md-12 mb-5" style={{ textAlign: "center" }}>
                <h2>My Private Tokens</h2>
              </div>
            </div>
            <div className="row">
              {this.props.tokens.map(el => (
                <div key={el.uid} className="col-md-4">
                  <div
                    className="shadow-sm mb-4 card"
                    style={{ width: "18rem" }}
                  >
                    <img className="card-img-top m-3 pr-4" src={UI[el.uid]} />
                    <div className="card-body">
                      <div className="d-flex justify-content-between align-items-center">
                        <div className="btn-group">
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() => this.props.fetchMerkleProof(el.uid)}
                          >
                            Verify
                          </button>
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-secondary"
                            onClick={() =>
                              this.props.sendToken(
                                [
                                  process.env.ALICE_PK_X,
                                  process.env.ALICE_PK_Y
                                ],
                                el.uid
                              )
                            }
                          >
                            Private Send
                          </button>
                        </div>
                        <small className="text-muted">
                          {el.verified ? "✅ Verified" : "Not Verified"}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const MerkleRoot = connect(
  mapStateToProps,
  mapDispatchToProps
)(ConnectedMerkleRoot);

ConnectedMerkleRoot.propTypes = {
  fetchMerkleRoot: PropTypes.func.isRequired
};

export default MerkleRoot;
