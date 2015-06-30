var path = require('path');
var webpack = require('webpack');
var build = require('webpack-build');
var autoprefixer = require('autoprefixer-core');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = function(opts) {
	var config = {
		context: __dirname,
		entry: './app',
		output: {
			filename: '[name]-[hash].js'
		},
		module: {
			loaders: [
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
		plugins: [
			new webpack.optimize.OccurrenceOrderPlugin(),
			new webpack.NoErrorsPlugin()
		]
	};

	if (opts.hmr && !opts.context.DEBUG) {
		// Enable hmr of react components and stylesheets
		config.module.loaders.push(
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'react-hot-loader!babel-loader'
			},
			{
				test: /\.css$/,
				loader: 'style!css?sourceMap!postcss'
			}
		);
	} else {
		config.module.loaders.push(
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel-loader'
			},
			// Move css assets into separate files
			{
				test: /\.css$/,
				loader: ExtractTextPlugin.extract('style', 'css?sourceMap!postcss')
			}
		);

		config.plugins.push(
			new ExtractTextPlugin('[name]-[contenthash].css')
		);
	}

	if (opts.context.DEBUG) {
		config.devtool = 'inline-source-map';

		config.output.pathinfo = true;

		config.plugins.push(
			new webpack.DefinePlugin({
				'process.env': {
					NODE_ENV: JSON.stringify('development')
				}
			})
		);
	} else {
		config.devtool = 'source-map';

		config.plugins.push(
			new webpack.optimize.DedupePlugin(),
			new webpack.DefinePlugin({
				'process.env': {
					NODE_ENV: JSON.stringify('production')
				}
			})
		);
	}

	return config;
};