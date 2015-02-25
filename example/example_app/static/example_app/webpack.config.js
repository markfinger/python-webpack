var path = require('path');

module.exports = {
    context: __dirname,
	entry: './example',
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};