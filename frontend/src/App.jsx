import React, { Component } from 'react';
import { req } from './requests';
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

  request = (path) => {
    const { email, password } = this.state;
    if (path === 'login') {
      req(path, { email, password }, (res) => {
        console.log(res);
      });
    }
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
