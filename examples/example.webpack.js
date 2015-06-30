var path = require('path');
var webpack = require('webpack');
var build = require('webpack-build');
var autoprefixer = require('autoprefixer-core');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = function(opts) {
	var jsLoader = {
		test: /\.jsx?$/,
		exclude: /(node_modules|bower_components)/,
		loaders: ['babel-loader']
	};

	var cssLoader = {
		test: /\.css$/,
		loaders: ['css-loader?sourceMap', 'postcss-loader']
	};

	var config = {
		context: __dirname,
		entry: './app',
		output: {
			filename: '[name]-[hash].js'
		},
		module: {
			loaders: [
				jsLoader,
				cssLoader,
				{
					test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
					loaders: ['url-loader?limit=10000&mimetype=application/font-woff']
				},
				{
					test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
					loaders: ['file-loader']
				}
			]
		},
		postcss: [autoprefixer],
		plugins: [
			new webpack.optimize.OccurrenceOrderPlugin(),
			new webpack.NoErrorsPlugin()
		]
	};

	if (opts.hmr) {
		// Enable hmr of react components and stylesheets
		jsLoader.loaders.unshift('react-hot-loader');
		cssLoader.loaders.unshift('style');
	} else {
		// Move css assets into separate files
		cssLoader.loader = ExtractTextPlugin.extract('style', cssLoader.loaders.join('!'));
		delete cssLoader.loaders;
		config.plugins.push(new ExtractTextPlugin('[name]-[contenthash].css'));
	}

	if (opts.context.DEBUG) {
		config.devtool = 'eval-source-map';
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
			}),
			new webpack.optimize.UglifyJsPlugin()
		);
	}

	return config;
};