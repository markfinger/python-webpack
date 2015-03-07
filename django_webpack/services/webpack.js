var fs = require('fs');
var path = require('path');
var webpack = require('webpack');
var Watchpack = require('watchpack');
var WebpackWatcher = require('webpack-watcher');
var tmp = require('tmp');

var bundles = {};
var watchedConfigFiles = [];
var configWatcher = null;

var getBundle = function(options) {
	if (bundles[options.pathToConfig] === undefined) {
		bundles[options.pathToConfig] = {
			pathToConfig: options.pathToConfig,
			config: null,
			output: null,
			generated: false,
			pendingResponses: [],
			watchingConfig: false
		};
	}
	return bundles[options.pathToConfig];
};

var getConfigWatcher = function() {
	if (!configWatcher) {
		configWatcher = new Watchpack();
		configWatcher.on('change', function(filePath) {
			if (filePath in bundles) {
				var bundle = bundles[filePath];
				invalidateConfig(bundle);
			}
		});
	}
	return configWatcher;
};

var sendErrorResponse = function(response, error) {
	if (error instanceof Error) {
		console.error(error);
	} else {
		console.error(new Error(error));
	}
	response.status(500).send(error);
};

var sendPendingResponses = function(bundle) {
	var output;

	var pendingResponses = bundle.pendingResponses;
	bundle.pendingResponses = [];

	if (bundle.error) {
		pendingResponses.forEach(function(response) {
			return sendErrorResponse(response, bundle.error);
		});
	} else {
		output = JSON.stringify(bundle.output);
		pendingResponses.forEach(function(response) {
			response.send(output);
		});
	}
};

var invalidateBundle = function(bundle) {
	bundle.generated = false;
	// TODO: invalidate bundle watcher
};

var invalidateConfig = function(bundle) {
	delete require.cache[bundle.pathToConfig];
	bundle.config = null;
	invalidateBundle(bundle);
};

var requireConfig = function(options, response) {
	try {
		var config = require(options.pathToConfig);
	} catch(e) {
		return sendErrorResponse(response, e);
	}

	if (!config) {
		return sendErrorResponse(response, 'Config file "' + options.pathToConfig + '" does not export an object.');
	}

	if (config.output && config.output.path) {
		config.output.path = config.output.path.replace('{{ BUNDLE_ROOT }}', options.bundleRoot);
	}

	return config;
};

var watchConfigFile = function(pathToConfigFile) {
	if (watchedConfigFiles.indexOf(pathToConfigFile) === -1) {
		watchedConfigFiles.push(pathToConfigFile);
	}
	var configWatcher = getConfigWatcher();
	configWatcher.watch(watchedConfigFiles, []);
};

var getConfig = function(options, response) {
	var bundle = getBundle(options);

	if (!bundle.config) {
		bundle.config = requireConfig(options, response);
	}

	if (options.watchConfigFiles && !bundle.watchingConfig) {
		watchConfigFile(bundle.pathToConfig);
		bundle.watchingConfig = true
	}

	return bundle.config;
};

var generateBundle = function(options, response) {
	var bundle = getBundle(options);
	bundle.pendingResponses.push(response);

	if (bundle.generated) {
		return sendPendingResponses(bundle);
	}

	var config = getConfig(options, response);

	if (!config) {
		console.error(new Error('Config "' + options.pathToConfig + '" can not be built'));
		return;
	}

	webpack(config, function(err, stats) {
		if (err) {
			console.error(new Error(err));
			response.status(500).send(err);
			bundle.error = err;
			return sendPendingResponses(bundle);
		} else {
			bundle.error = null;
		}

		var statsToJsonOptions;
		if (!options.outputFullStats) {
			// Minimise the amount of data that needs to sent back by omitting
			// some statistics from the build.
			// Ref: http://webpack.github.io/docs/node.js-api.html#stats-tojson
			statsToJsonOptions = {
				modules: false,
				source: false
			};
		}
		bundle.output = {
			config: config,
			stats: stats.toJson(statsToJsonOptions)
		};

		bundle.generated = true;

		sendPendingResponses(bundle);
	});
};

var service = function service(request, response) {
	var pathToConfig = request.query.path_to_config;

	var bundleRoot = request.query.bundle_root;
	if (!bundleRoot) {
		return sendErrorResponse(response, 'No bundle_root option was provided');
	}

	if (request.query.watch_config_files === undefined) {
		return sendErrorResponse(response, 'No watch_config_files option was provided');
	}
	var watchConfigFiles = request.query.watch_config_files === 'True';

	if (request.query.output_full_stats === undefined) {
		return sendErrorResponse(response, 'No output_full_stats option was provided');
	}
	var outputFullStats = request.query.output_full_stats === 'True';

	var options = {
		pathToConfig: pathToConfig,
		bundleRoot: bundleRoot,
		watchConfigFiles: watchConfigFiles,
		outputFullStats: outputFullStats
	};

	generateBundle(options, response);
};

module.exports = service;