import React from 'react';

export default React.createClass({
	render() {
		return (
			<div>
				<h3>{this.props.author}</h3>
				{this.props.text}
			</div>
		);
	}
});