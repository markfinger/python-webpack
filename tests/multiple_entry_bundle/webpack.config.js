var path = require('path');

module.exports = {
	context: __dirname,
	entry: ['./entry_1/entry', './entry_2/entry', './entry_3/entry', './entry_4/entry', './entry_5/entry'],
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};