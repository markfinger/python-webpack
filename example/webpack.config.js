var path = require('path');
var webpack = require('webpack');
var builds = require('webpack-wrapper/lib/builds');
var autoprefixer = require('autoprefixer-core');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: './app',
    output: {
        filename: '[name]-[hash].js'
    },
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'react-hot-loader!babel-loader'
			},
			{
				test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "url-loader?limit=10000&mimetype=application/font-woff"
			},
			{
				test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
				loader: "file-loader"
			}
		]
	},
	postcss: [autoprefixer],
	builds: {
    dev: function(config, opts) {
      // Activate hmr and performant source maps

      config = builds.dev(config, opts);

      // Enable hmr of stylesheets
      config.module.loaders.push({
        test: /\.css$/,
        loader: 'style-loader!css-loader!postcss-loader'
      });

      return config;
    },
    prod: function(config, opts) {
      // Minify and move css assets into separate files

      config = builds.prod(config, opts);

      config.module.loaders.push({
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader!postcss-loader')
      });

      config.plugins.push(
        new ExtractTextPlugin('[name]-[hash].css')
      );

      return config;
    }
  }
};