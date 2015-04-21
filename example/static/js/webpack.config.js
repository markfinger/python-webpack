var path = require('path');

module.exports = {
    context: __dirname, 
    entry: './main',
    output: {
		path: '[bundle_dir]',
        filename: 'bundle-[hash].js'
    },
	devtool: 'eval'
};