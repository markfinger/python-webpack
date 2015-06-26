import React from 'react';
import CommentBox from './CommentBox.jsx';

let render = (comments, handleNewComment) => {
  	React.render(
		<CommentBox	comments={comments} handleNewComment={handleNewComment} />,
		document.getElementsByClassName('container')[0]
	);
};

let comments = [];

let handleNewComment = (comment) => {
	comments.push(comment);
	render(comments, handleNewComment);
};

render(comments, handleNewComment);

