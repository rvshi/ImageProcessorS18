import React, { Component } from 'react';
import { req, validate } from '../requests';
import Login from './Login';
import Dashboard from './Dashboard';
import Notifications from './Notifications';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      jwt: null,
      loggedIn: false
    };
  }

  componentDidMount() {
    const jwt = localStorage.getItem('jwt');
    let loggedIn = false;
    let username = '';

    if (jwt !== 'null' && jwt !== 'undefined') {
      validate(jwt, (res, success) => {
        if (success) {
          loggedIn = true;
          username = res.data.username;
        } else {
          localStorage.setItem('jwt', 'undefined'); // remove jwt
        }
        this.setState({ jwt, username, loggedIn });
      });
    }
  }

  update = (key, val) => {
    this.setState({ [key]: val });
  }

  notify = (message, type) => {
    // type is either 'good' or 'bad'
    this.setState({ 'notification': { message, type } });
    setTimeout(() => { this.setState({ 'notification': null }); }, 3500);
  }

  logout = () => {
    this.setState({
      username: '',
      jwt: null,
      loggedIn: false
    });
    localStorage.setItem('jwt', 'undefined'); // remove jwt
  }

  request = (path) => {
    const { username, password } = this.state;
    if (path === 'login') {
      req(null, path, { username, password }, (res, success) => {
        if (success) {
          const jwt = res.data.jwt;
          localStorage.setItem('jwt', jwt);
          this.setState({ 'jwt': jwt, 'loggedIn': true });
          this.notify(`Welcome back ${username}!`, 'good');
        } else {
          this.notify('Username or password are incorrect.', 'bad');
        }
      });
    }
  }

  render() {
    const { username, password, loggedIn, notification } = this.state;
    return (
      <div className="App">
        {loggedIn ?
          <Dashboard update={this.update} request={this.request} logout={this.logout} username={username} />
          : <Login update={this.update} request={this.request} username={username} password={password} />
        }
        {notification && <Notifications notification={notification} />}
      </div>
    );
  }
}

export default App;
