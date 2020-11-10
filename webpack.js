const path = require('path');

module.exports = {
  entry: {
    'index': './js/index.js',
    'register': './js/register.js',
    'activity': './js/activity.js',
  },
  output: {
    path: path.resolve(__dirname, 'build/'),
    filename: 'js/[name].js'
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
      },
    ]
  },
  devtool: 'source-map'
};