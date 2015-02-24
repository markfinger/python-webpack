var path = require('path');

module.exports = {
	context: __dirname,
	entry: ['./entry_1/entry', './entry_2/entry'],
    output: {
        path: path.join(__dirname, '..', 'static_root', 'bundles'),
        filename: 'bundle-[hash].js'
    }
};