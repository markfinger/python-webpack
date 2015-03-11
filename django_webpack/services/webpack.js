var fs = require('fs');
var path = require('path');
var mkdirp = require('mkdirp');
var webpack = require('webpack');
var Watchpack = require('watchpack');
var WebpackWatcher = require('webpack-watcher');
var tmp = require('tmp');
var _ = require('lodash');

var bundles = [];
var watchedConfigFiles = [];
var configWatcher = null;

var logger = function() {
	console.log(Array.prototype.slice.call(arguments));
};

var getBundle = function(options) {
	var bundle = _.find(bundles, {
		pathToConfig: options.pathToConfig,
		watchConfig: options.watchConfig,
		watchSource: options.watchSource,
		outputFullStats: options.outputFullStats
	});
	if (!bundle) {
		bundle = {
			pathToConfig: options.pathToConfig,
			watchConfig: options.watchConfig,
			watchSource: options.watchSource,
			outputFullStats: options.outputFullStats,
			config: null,
			output: null,
			generated: false,
			pendingResponses: [],
			waitingForCompiler: false,
			watchingConfig: false,
			sourceWatcher: null,
			waitingForSourceWatcher: false
		};
		bundles.push(bundle);
	}
	return bundle;
};

var getConfigWatcher = function() {
	if (!configWatcher) {
		logger('Creating config watcher');
		configWatcher = new Watchpack();
		configWatcher.on('change', function(filePath) {
			var bundle = _.find(bundles, {
				pathToConfig: filePath,
				watchingConfig: true
			});
			logger('Change in config file', filePath);
			if (bundle) {
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
	if (bundle.generated) {
		bundle.generated = false;
		logger('Invalidated bundle', bundle.pathToConfig);
	}
};

var invalidateConfig = function(bundle) {
	delete require.cache[bundle.pathToConfig];
	bundle.config = null;
	invalidateBundle(bundle);
	if (bundle.sourceWatcher) {
		bundle.sourceWatcher.closeWatcher();
		bundle.sourceWatcher = null;
	}
	logger('Invalidated config', bundle.pathToConfig);
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
		config.output.path = config.output.path.replace('[bundle_dir]', options.bundleDir);
	}

	return config;
};

var watchBundleConfigFile = function(bundle) {
	if (watchedConfigFiles.indexOf(bundle.pathToConfig) === -1) {
		watchedConfigFiles.push(bundle.pathToConfig);
	}
	var configWatcher = getConfigWatcher();
	configWatcher.watch(watchedConfigFiles, []);
	bundle.watchingConfig = true;
	logger('Watching config file', bundle.pathToConfig);
};

var getConfig = function(options, response) {
	var bundle = getBundle(options);

	if (!bundle.config) {
		bundle.config = requireConfig(options, response);
	}

	if (bundle.watchConfig && !bundle.watchingConfig) {
		watchBundleConfigFile(bundle);
	}

	return bundle.config;
};

var generateBundleOutput = function(options, config, stats) {
	var bundle = getBundle(options);

	var statsToJsonOptions;
	if (!bundle.outputFullStats) {
		// Minimise the amount of data that needs to sent back by omitting
		// some statistics from the build.
		// Ref: http://webpack.github.io/docs/node.js-api.html#stats-tojson
		statsToJsonOptions = {
			modules: false,
			source: false
		};
	}

	return {
		pathToConfig: bundle.pathToConfig,
		config: config,
		stats: stats.toJson(statsToJsonOptions),
		watchSource: bundle.watchSource,
		watchConfig: bundle.watchConfig,
		outputGeneratedAt: new Date()
	};
};

var getSourceWatcher = function(options) {
	var bundle = getBundle(options);

	if (!bundle.sourceWatcher) {
		// TODO: catch errors which are killing the server, multi entries pointing to non-existent files triggers a fatal error
		var config = getConfig(options);
		var compiler = webpack(config, function(err) {
			if (err) {
				console.error(new Error(err));
				bundle.error = err;
				sendPendingResponses(bundle);
			}
		});
		var onError = function(err) {
			if (err) {
				console.error(new Error(err));
				bundle.error = err;
				sendPendingResponses(bundle);
			}
		};
		bundle.sourceWatcher = new WebpackWatcher(compiler, {
			onInvalid: function() {
				invalidateBundle(bundle);
			},
			onDone: function(stats) {
				if (stats.hasErrors()) {
					var err = stats.errors;
					onError(err);
				} else {
					bundle.error = null;
				}
				invalidateBundle(bundle);
			},
			onError: onError
		});
	}

	return bundle.sourceWatcher;
};

var generateBundle = function(options, response) {
	var bundle = getBundle(options);
	bundle.pendingResponses.push(response);

	if (bundle.generated) {
		logger('Already generated bundle', bundle.pathToConfig);
		return sendPendingResponses(bundle);
	}

	var config = getConfig(options, response);

	if (!config) {
		console.error(new Error('Config "' + options.pathToConfig + '" can not be built'));
		return;
	}

	if (bundle.watchSource) {
		if (!bundle.waitingForSourceWatcher) {
			logger('Requesting bundle from source watcher', bundle.pathToConfig);
			bundle.waitingForSourceWatcher = true;
			var watcher = getSourceWatcher(options);
			watcher.onReady(function (stats) {
				logger('Source watcher onReady', bundle.pathToConfig);

				bundle.waitingForSourceWatcher = false;
				bundle.generated = true;
				bundle.output = generateBundleOutput(bundle, config, stats);

				// Write the files from memory to disk
				_.forIn(stats.compilation.assets, function (asset) {
					var content = watcher.readFileSync(asset.existsAt);
					try {
						mkdirp.sync(path.dirname(asset.existsAt));
						fs.writeFileSync(asset.existsAt, content);
					} catch (err) {
						bundle.error = err;
						// Escape the for loop
						return false;
					}
				});

				sendPendingResponses(bundle);
			});
		} else {
			logger('Waiting for source watcher', bundle.pathToConfig);
		}
	} else if (!bundle.waitingForCompiler) {
		logger('Starting compiler', bundle.pathToConfig);
		bundle.waitingForCompiler = true;
		webpack(config, function(err, stats) {
			bundle.waitingForCompiler = false;
			if (err) {
				console.error(new Error(err));
				bundle.error = err;
				sendPendingResponses(bundle);
				return;
			} else {
				bundle.error = null;
			}
			bundle.output = generateBundleOutput(bundle, config, stats);
			bundle.generated = true;
			sendPendingResponses(bundle);
		});
	} else {
		logger('Waiting for compiler', bundle.pathToConfig);
	}
};

var service = function service(data, response) {
	if (!data.bundle_dir) {
		return sendErrorResponse(response, 'No bundle_dir option was provided');
	}

	var options = {
		pathToConfig: data.path_to_config,
		bundleDir: data.bundle_dir,
		watchConfig: data.watch_config,
		watchSource: data.watch_source,
		outputFullStats: data.output_full_stats
	};

	generateBundle(options, response);
};

module.exports = service;