class BibtexEntry extends React.Component {
  constructor(props) {
    super(props);
    this.state = {expanded: false};

    this.handleClick = this.handleClick.bind(this);
  }
  handleClick(e) {
    e.preventDefault();
    this.setState({expanded: !this.state.expanded})
  }
  render() {
    if (this.state.expanded) {
    return (
      <div>
      <div>
        <span dangerouslySetInnerHTML={this.props.authors}></span>. <b><a href={ this.props.url }>{ this.props.title }</a></b>. <i>{ this.props.source }</i>, { this.props.year }. <a onClick={this.handleClick}>[bibtex]</a>
      </div>
      <div>Bibtex info</div>
      </div>
    );
    } else {
    return (
      <div>
        <span dangerouslySetInnerHTML={this.props.authors}></span>. <b><a href={ this.props.url }>{ this.props.title }</a></b>. <i>{ this.props.source }</i>, { this.props.year }. <a onClick={this.handleClick}>[bibtex]</a>
      </div>
    );
    }
  }
}

for (const e of document.getElementsByClassName("bibtex")) {
  const author_html = {__html: e.dataset.authors};
  ReactDOM.render(
    <BibtexEntry
    authors={author_html}
    url={e.dataset.url}
    title={e.dataset.title}
    source={e.dataset.source}
    year={e.dataset.year}
     />,
    e
  );
}
