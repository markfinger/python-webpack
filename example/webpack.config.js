var path = require('path');
var webpack = require('webpack');
var build = require('webpack-build');
var autoprefixer = require('autoprefixer-core');
var csswring = require('csswring');
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
		postcss: [autoprefixer]
	};

	if (opts.hmr) {
		// Enable hmr of stylesheets
		config.module.loaders.push({
			test: /\.css$/,
			loader: 'style!css!postcss'
		});
	} else {
		// Move css assets into separate files
		config.module.loaders.push({
			test: /\.css$/,
			loader: ExtractTextPlugin.extract('style', 'css?-minimize&sourceMap!postcss')
		});

		config.plugins.push(
			new ExtractTextPlugin('[name]-[contenthash].css')
		);
	}

	if (opts.context.DEBUG) {
		// TODO: remove this in favour of explicit additions
		build.env.dev(config, opts);
	} else {
		// TODO: remove this in favour of explicit additions
		build.env.prod(config, opts);

		// TODO: this was needed at one point for source-maps, should check if it's still the case
		// Compress CSS with csswring, rather than using webpack's clean-css
		config.postcss.push(csswring);
	}

	return config;
};