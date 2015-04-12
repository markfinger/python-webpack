var webpackService = require('webpack-service');

module.exports = function(data, response) {
	if (!data.bundleDir) {
		return response.status(500).end('No bundle_dir option was provided');
	}

	webpackService(data, function(err, stats) {
		if (err) {
			return response.status(500).end(err.stack || err);
		}
		response.end(JSON.stringify(stats));
	});
};