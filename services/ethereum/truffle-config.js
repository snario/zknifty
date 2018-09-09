module.exports = {
  networks: {
    testrpc: {
      host: "0.0.0.0",
      port: 8545,
      network_id: 7777777,
      gasPrice: 1,
    },
  },
  compilers: {
    solc: {
      settings: {
       optimizer: {
         enabled: true,
         runs: 20
       },
      }
    }
  }
}
