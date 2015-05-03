var webpackService = require('webpack-service');

module.exports = {
	functions: {
		webpack: webpackService
	},
	// Ensure that the host and manager shut down immediately when the python
	// process does
	disconnectTimeout: 0
};