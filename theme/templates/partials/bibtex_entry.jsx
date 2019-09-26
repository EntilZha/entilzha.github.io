class BibtexEntry extends React.Component {
  constructor(props) {
    super(props);
    this.state = { expanded: false };
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick(e) {
    e.preventDefault();
    this.setState({ expanded: !this.state.expanded });
  }
  render() {
    if (this.state.expanded) {
      return (
        <span>
          <a href="#" onClick={this.handleClick}>
            [bibtex]
          </a>
          <div className="alert alert-primary" style={{ whiteSpace: "pre-wrap" }}>
            {this.props.entry}
          </div>
        </span>
      );
    } else {
      return (
        <a href="#" onClick={this.handleClick}>
          [bibtex]
        </a>
      );
    }
  }
}
docReady(function() {
  for (const e of document.getElementsByClassName("bibtex")) {
    ReactDOM.render(<BibtexEntry entry={e.dataset.entry} />, e);
  }
});
