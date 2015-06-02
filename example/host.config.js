var webpack = require('webpack-wrapper');

module.exports = {
	functions: {
		webpack: webpack
	},
	extendHost: function(host) {
		webpack.hmr.addTo(host.server);
	}
};