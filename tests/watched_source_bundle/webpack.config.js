
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry.js',
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};
