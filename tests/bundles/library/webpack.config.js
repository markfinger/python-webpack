var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
	entry: './entry.js',
    output: {
        filename: 'bundle-[hash].js',
		library: 'LIBRARY_TEST'
    }
};