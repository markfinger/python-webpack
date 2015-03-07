var webpack = require('webpack');
var WebpackWatcher = require('webpack-watcher');

var bundles = {};

var getBundle = function(options) {
	if (bundles[options.pathToConfig] === undefined) {
		bundles[options.pathToConfig] = {
			pathToConfig: options.pathToConfig,
			config: null,
			output: null,
			generatingBundle: true,
			pendingResponses: []
		};
	}
	return bundles[options.pathToConfig];
};

var sendBundleResponses = function(bundle) {
	var pendingResponses = bundle.pendingResponses;
	bundle.pendingResponses = [];

	var output = bundle.output;
	var jsonOutput = JSON.stringify(output);

	pendingResponses.forEach(function(response) {
		response.send(jsonOutput);
	});
};

var sendErrorResponse = function(response, error) {
	if (error instanceof Error) {
		console.error(error);
	} else {
		console.error(new Error(error));
	}
	response.status(500).send(error);
};

var getConfig = function(options, response) {
	var bundle = getBundle(options);

	if (!bundle.config || !options.cacheConfigFiles) {
		// Ensure that config files are not cached in development
		if (options.pathToConfig in require.cache) {
			delete require.cache[options.pathToConfig];
		}
		try {
			var config = require(options.pathToConfig);
		} catch(e) {
			return sendErrorResponse(response, e);
		}
		// Ensure that the config exports something
		if (!config) {
			return sendErrorResponse(response, 'Config file "' + options.pathToConfig + '" does not exports an object.');
		}
		if (config.output && config.output.path) {
			config.output.path = config.output.path.replace('{{ BUNDLE_ROOT }}', options.bundleRoot);
		}
		bundle.config = config;
	}

	return config;
};

var generateBundle = function(options, response) {
	var bundle = getBundle(options);
	bundle.pendingResponses.push(response);

	if (!bundle.generatingBundle) {
		return sendBundleResponses(bundle);
	}

	var config = getConfig(options, response);
	if (!config) {
		// An error was encountered and an error response will have been sent
		return;
	}

	webpack(config, function(err, stats) {
		if (err) {
			console.error(new Error(err));
			response.status(500).send(err);
			bundle.error = err;
			return;
		} else {
			bundle.error = null;
		}
		// TODO: pass out the assets, errors, and warnings, the stats toJson object has too much data in it
		// TODO: limit the json output: http://webpack.github.io/docs/node.js-api.html#stats-tojson
		bundle.output = {
			config: config,
			stats: stats.toJson()
		};
		bundle.generatingBundle = false;
		sendBundleResponses(bundle);
	});
};

var service = function service(request, response) {
	var pathToConfig = request.query.path_to_config;

	if (!request.query.cache_config_files === undefined) {
		return sendErrorResponse(response, 'No cache_config_files option was provided');
	}
	var cacheConfigFiles = request.query.cache_config_files === 'True';

	var bundleRoot = request.query.bundle_root;
	if (!bundleRoot) {
		return sendErrorResponse(response, 'No bundle_root option was provided');
	}

	var options = {
		cacheConfigFiles: cacheConfigFiles,
		bundleRoot: bundleRoot,
		pathToConfig: pathToConfig
	};

	generateBundle(options, response);
};

module.exports = service;