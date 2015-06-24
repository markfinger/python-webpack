var path = require('path');

module.exports = function() {
	return {
		context: __dirname,
		entry: {
			bundle_1: './bundle_1/entry',
			bundle_2: './bundle_2/entry'
		},
		output: {
			filename: 'bundle-[name].js'
		}
	}
};