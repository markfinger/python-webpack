
var path = require('path');

module.exports = {
    context: path.join(__dirname, 'app'),
    entry: './entry2.js',
    output: {
        path: '[bundle_dir]',
        filename: 'bundle-[hash].js'
    }
};
