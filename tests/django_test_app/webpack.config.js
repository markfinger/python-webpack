var path = require('path');

module.exports = function() {
	return {
		context: path.join(__dirname, 'static', 'django_test_app'),
		entry: './entry.js',
		output: {
			filename: 'bundle-[hash].js'
		}
	};
};