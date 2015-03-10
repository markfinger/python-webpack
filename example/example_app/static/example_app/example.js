var $ = require('jquery');
var insertCat = require('./insert-cat');

console.log('Hello, I am the example bundle');

$(function() {
	$('<h1>Hello, World!</h1>')
		.appendTo('body')
		.css({
			margin: 10,
			'text-align': 'center',
			'font-size': 30,
			'font-weight': 'bold'
		});

	var catText = $('<h2>')
		.appendTo('body')
		.css({
			position: 'absolute',
			top: 0,
			bottom: 0,
			margin: 'auto',
			height: 30,
			width: '100%',
			'text-align': 'center',
			'font-size': 30,
			'font-weight': 'bold'
		});

	insertCat(catText);
});