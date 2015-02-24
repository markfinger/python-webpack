var path = require('path');

module.exports = {
	context: __dirname,
	entry: {
		bundle_1: './bundle_1/entry',
		bundle_2: './bundle_2/entry'
	},
    output: {
        path: path.join(__dirname, '..', 'static_root', 'bundles'),
        filename: 'bundle-[name].js'
    }
};