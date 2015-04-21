var path = require('path');

module.exports = {
    context: __dirname,
	entry: './entry.js',
    output: {
        path: '[bundle_dir]',
        filename: 'bundle-[hash].js'
    }
};