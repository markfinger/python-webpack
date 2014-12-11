var fs = require('fs');
var path = require('path');
var argv = require('yargs').argv;
var webpack = require('webpack');

var entry = argv.entry;
if (!entry) {
	throw new Error('No entry point specified for the bundle, ex: `--entry=/path/to/some/file.js`');
}

if (!fs.existsSync(entry)) {
    throw new Error('Cannot find entry file "' + entry + '"');
}

var output = argv.output;
if (!output) {
	throw new Error('No output path specified for the bundle, ex: `--output=/path/to/some/file.js`');
}

var library = argv.library;

var externals = argv.externals;
if (externals) {
	externals = JSON.parse(externals);
}

var loaders = argv.loaders;
if (loaders) {
	// Serialise the loaders and convert the conditions to regex instances
	loaders = JSON.parse(loaders);
	var conditions = ['test', 'include', 'exclude'];
	loaders = loaders.map(function(loader) {
		conditions.forEach(function(condition) {
			if (loader.hasOwnProperty(condition)) {
				loader[condition] = new RegExp(loader[condition]);
			}
		});
		return loader;
	});
}

var pathsToLoaders = argv.pathsToLoaders;
if (pathsToLoaders) {
	pathsToLoaders = pathsToLoaders.split(':');
}

var noParse = argv.noParse;
if (noParse) {
	noParse = JSON.parse(noParse);
	noParse = noParse.map(function(regex) {
		return new RegExp(regex);
	});
}

var devtool = argv.devtool;

var bail = argv.bail !== undefined;

webpack({
    entry: entry,
    output: {
        filename: output,
		library: library
    },
	externals: externals,
	module: {
		loaders: loaders,
		noParse: noParse
	},
	resolveLoader: {
		root: pathsToLoaders
	},
	devtool: devtool,
	bail: bail
}, function(err, stats) {
    if (err) {
		throw new Error(err);
	}
    var jsonStats = stats.toJson();
    if (jsonStats.errors.length) {
		throw new Error(jsonStats.errors);
	}
	var paths = Object.keys(stats.compilation.assets);
	console.log(paths[0]);
});