var webpack = require('webpack');

var cachedConfigFiles = {};

var service = function(request, response) {
	var pathToConfig = request.query.path_to_config;

	// Ensure that config files are not cached during development
	var cache = request.query.cache === 'True';
	if (!cache && cachedConfigFiles[pathToConfig] !== undefined) {
		delete require.cache[pathToConfig];
	}

	var config = require(pathToConfig);

	if (!cache) {
		cachedConfigFiles[pathToConfig] = true;
	}

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