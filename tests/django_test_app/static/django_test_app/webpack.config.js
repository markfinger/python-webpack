var path = require('path');

module.exports = function() {
	return {
		context: __dirname,
		entry: './entry.js',
		output: {
			filename: 'bundle-[hash].js'
		}
	};
};