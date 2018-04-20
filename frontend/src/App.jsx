import React, { Component } from 'react';

import Login from './Login';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: ''
    };
  }

  update = (key, val) => {
    this.setState({ [key]: val });
  }

  request = (name) => {
    // make requests via axios
  }

  render() {
    const { email, password } = this.state;
    return (
      <div className="App">
        <Login update={this.update} request={this.request} email={email} password={password} />
        <div className="bg" />
      </div>
    );
  }
}

export default App;
