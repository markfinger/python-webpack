import 'bootstrap/dist/css/bootstrap.css';
import './CommentBox.css'
import React from 'react';
import CommentList from './CommentList.jsx';
import CommentForm from './CommentForm.jsx';

export default React.createClass({
	render() {
		return (
			<div>
				<CommentList comments={this.props.comments} />
				<CommentForm url={this.props.url} onCommentSubmit={this.props.handleNewComment} />
			</div>
		);
	}
});