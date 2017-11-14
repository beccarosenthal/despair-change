"use strict";

class Hello extends React.Component {
    render() {
        return <p>Hi { this.props.to } from { this.props.from }</p>
    }
class Hello extends React.Component {
    render() {
        return <p>Hi { this.props.to } from { this.props.from }</p>
    }
class TodoList extends React.Component {
  render() {
      return <div>
        <h4>Here is a todo list that you may or may not follow</h4>
        <p>in a future life, you may be able to follow to do lists</p>
        <ul>
            <TodoItem item="figure out database transaction thing" important={true}/>
            <TodoItem item="read the dictionary from a-z" important={false}/>
            <TodoItem item="save the rainforest" important={false}/>
        </ul>
        </div>
  }
}


class TodoItem extends React.Component {
  render() {
        if (this.props.important === true) {
            return <b><li>{this.props.item}</li></b>
        } else {
            return <li>{this.props.item}</li>
        }

  }
}
