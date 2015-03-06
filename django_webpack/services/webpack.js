var webpack = require('webpack');
var WebpackWatcher = require('webpack-watcher');

var errorResponse = function(response, error) {
	if (error instanceof Error) {
		console.error(error);
	} else {
		console.error(new Error(error));
	}
	response.status(500).send(error);
};

var processConfig = function(request, config) {
	var bundleRoot = request.query.bundle_root;
	if (!bundleRoot) {
		return errorResponse(response, 'No bundle_root option was provided');
	}
	if (config.output && config.output.path) {
		config.output.path = config.output.path.replace('{{ BUNDLE_ROOT }}', bundleRoot);
	}
	return config;
};

var generateBundle = function(request, response, pathToConfig) {
	try {
		var config = require(pathToConfig);
	} catch(e) {
		return errorResponse(response, e);
	}

	if (config === undefined) {
		return errorResponse(response, 'Config file "' + pathToConfig + '" exports undefined.');
	}

	config = processConfig(request, config);

	webpack(config, function(err, stats) {
		if (err) {
			console.error(new Error(err));
			response.status(500).send(err);
			return;
		}
		// TODO: pass out the assets, errors, and warnings, the stats toJson object has too much data in it
		// TODO: limit the json output: http://webpack.github.io/docs/node.js-api.html#stats-tojson
		var output = {
			config: config,
			stats: stats.toJson()
		};
		response.send(JSON.stringify(output));
	});
};

var service = function(request, response) {
	var pathToConfig = request.query.path_to_config;

	// Ensure that config files are not cached during development
	var cache = request.query.cache === 'True';
	if (!cache && pathToConfig in require.cache) {
		delete require.cache[pathToConfig];
	}

	//if (cache) {
		generateBundle(request, response, pathToConfig);
	//} else {
	//
	//}

};

module.exports = service;