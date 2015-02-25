var $ = require('jquery');
var catAsciiFaces = require('cat-ascii-faces');

var cats = catAsciiFaces.cats;
var catIndex = 0;
var catText = $('<h2>');

var insertCat = function() {
	catText.text(cats[catIndex]);
	catIndex++;
	if (catIndex > cats.length - 1) {
		catIndex = 0;
	}
	setTimeout(insertCat, 300);
};

$(function() {
	$('<h1>Hello, World!</h1>')
		.appendTo('body')
		.css({
			margin: 10,
			'text-align': 'center',
			'font-size': 30,
			'font-weight': 'bold'
		});

	catText
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

	insertCat();
});