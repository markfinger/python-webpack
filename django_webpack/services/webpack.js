var webpack = require('webpack');

var service = function(request, response) {
	var pathToConfig = request.query.path_to_config;
	var config = require(pathToConfig);

	webpack(config, function(err, stats) {
		if (err) {
			throw new Error(err);
		}
		response.send(
			JSON.stringify(stats.toJson())
		);
	});
};

module.exports = service;