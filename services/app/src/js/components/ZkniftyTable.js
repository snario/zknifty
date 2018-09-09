import React, { Component } from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import ethers from "ethers";

import { fetchMerkleRoot, fetchMyTokens, fetchMerkleProof } from "../actions";

const mapDispatchToProps = dispatch => {
  return {
    fetchMerkleRoot: () => dispatch(fetchMerkleRoot()),
    fetchMyTokens: () => dispatch(fetchMyTokens()),
    fetchMerkleProof: (uid) => dispatch(fetchMerkleProof(uid))
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

const UI = {
  0: "https://pbs.twimg.com/profile_images/1008479914612277248/xcnlNQOu_400x400.jpg",
  1: "https://pbs.twimg.com/profile_images/1008479914612277248/xcnlNQOu_400x400.jpg",
  2: "https://pbs.twimg.com/profile_images/1008479914612277248/xcnlNQOu_400x400.jpg",
  3: "https://pbs.twimg.com/profile_images/1008479914612277248/xcnlNQOu_400x400.jpg"
}

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
      <div>
        <p>Block Number: <code>{ blockNumber }</code></p>
        <p>Merkle Root: <code>{ this.props.merkleRoot }</code></p>
        <h2>My tokens</h2>
        <div className="row">
        {
          this.props.tokens.map(el => (
            <div key={ el.uid } className="mx-auto card" style={{"width": "18rem"}}>
              <img className="card-img-top" src={ UI[el.uid] }/>
              <div className="card-body">
                <h5 className="card-title">{ el.title }</h5>
                <a
                  onClick={ () => this.props.fetchMerkleProof(el.uid) }
                  className="card-link"
                  href="#"
                >
                  Verify
                </a>
                <a
                  onClick={ () => this.props.transferToken(el.uid) }
                  className="card-link"
                  href="#"
                >
                  Private Send
                </a>
              </div>
            </div>
          ))
        }
        </div>
      </div>
    );
  }
}

const MerkleRoot = connect(mapStateToProps, mapDispatchToProps)(ConnectedMerkleRoot);

ConnectedMerkleRoot.propTypes = {
  fetchMerkleRoot: PropTypes.func.isRequired
};

export default MerkleRoot;