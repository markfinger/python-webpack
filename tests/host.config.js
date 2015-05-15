var webpackWrapper = require('webpack-wrapper');

module.exports = {
	functions: {
		webpack: webpackWrapper
	},
	// Ensure that the host and manager shut down immediately when the python
	// process does
	disconnectTimeout: 0
};