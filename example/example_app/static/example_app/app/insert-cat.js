var catAsciiFaces = require('cat-ascii-faces');

var cats = catAsciiFaces.cats;
var catIndex = 0;

var insertCat = function(element) {
	element.text(cats[catIndex]);
	catIndex++;
	if (catIndex > cats.length - 1) {
		catIndex = 0;
	}
	setTimeout(function() {
		insertCat(element);
	}, 300);
};

module.exports = insertCat;
