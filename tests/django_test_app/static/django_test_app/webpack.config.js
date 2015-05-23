var path = require('path');

module.exports = {
    context: __dirname,
	entry: './entry.js',
    output: {
        filename: 'bundle-[hash].js'
    }
};