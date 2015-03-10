
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry1.js',
    output: {
        path: '{{ BUNDLE_ROOT }}',
        filename: 'bundle-[hash].js'
    }
};
