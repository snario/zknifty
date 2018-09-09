const webpack = require("webpack");
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader"
          }
        ]
      }
    ]
  },
  plugins: [
    new HtmlWebPackPlugin({
      template: "./src/index.html",
      filename: "./index.html"
    }),
    new webpack.DefinePlugin({
      'process.env': {
        ILLUMINATI_URL: JSON.stringify(process.env.ILLUMINATI_URL),
        ETHEREUM_JSONRPC_URL: JSON.stringify(process.env.ETHEREUM_JSONRPC_URL),
        MIXIMUS_ADDR: JSON.stringify(process.env.MIXIMUS_ADDR),
      }
    })
  ]
};
