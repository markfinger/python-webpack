var path = require('path');

module.exports = {
	context: __dirname,
	entry: ['./entry_1/entry', './entry_2/entry'],
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};