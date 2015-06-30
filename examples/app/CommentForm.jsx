import React from 'react';

export default React.createClass({
	handleSubmit(event) {
		event.preventDefault();

		this.props.onCommentSubmit({
			author: this.refs.author.getDOMNode().value.trim() || '...',
			text: this.refs.text.getDOMNode().value.trim() || '...'
		});

		this.refs.author.getDOMNode().value = '';
		this.refs.text.getDOMNode().value = '';
	},
	render() {
		return (
			<form onSubmit={this.handleSubmit}>
				<h2>Submit a comment</h2>
				<div className="form-group">
					<label>
						Your name
						<input type="text" className="form-control" ref="author" placeholder="..." />
					</label>
				</div>
				<div className="form-group">
					<label>
						Say something...
						<textarea className="form-control" ref="text" placeholder="..." />
					</label>
				</div>
				<div className="text-right">
					<button type="reset" className="btn btn-default">Reset</button>
					<button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>
		);
	}
});