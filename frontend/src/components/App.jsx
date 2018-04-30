import React, { Component } from 'react';
import { req, validate } from '../requests';
import Login from './Login';
import Dashboard from './Dashboard';
import Notifications from './Notifications';

const defaultState = {
  username: '',
  password: '',
  jwt: null,
  loggedIn: false,
  images: null
};
class App extends Component {
  constructor(props) {
    super(props);
    this.state = defaultState;
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

  update = (key, val, cb) => {
    if (cb) {
      this.setState({ [key]: val }, () => cb());
    } else {
      this.setState({ [key]: val });
    }
  }

  notify = (message, type) => {
    // type is either 'good' or 'bad'
    this.setState({ 'notification': { message, type } });
    setTimeout(() => { this.setState({ 'notification': null }); }, 3500);
  }

  logout = () => {
    this.setState(defaultState);
    localStorage.setItem('jwt', 'undefined'); // remove jwt
  }



  request = (path, options) => {

    const { jwt, username, password, images } = this.state;

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
    } else if (path === 'upload' && images && images.original) {
      req(jwt, path, { username, file: images.original }, (res, success) => {
        if (success) {
          const originalID = res.data.fileID;
          this.setState({ images: { ...images, originalID } });
          this.notify(`Image uploaded`, 'good');
        } else {
          this.notify('Error uploading image.', 'bad');
        }
      });
    } else if (path === 'process') {
      req(jwt, path, { username }, (res, success) => {
        if (success) {
          const processed = res.data.file;
          this.setState({ images: { ...images, processed } });
          this.notify(`Image processed`, 'good');
        } else {
          this.notify('Error processing image.', 'bad');
        }
      });
    } else if (path === 'download' && options) {
      req(jwt, path, { username, filetype: options }, (res, success) => {
        if (success) {
          const originalID = res.data.fileID;
          this.setState({ images: { ...images, originalID } });
          this.notify(`Image downloaded`, 'good');
        } else {
          this.notify('Error downloading image.', 'bad');
        }
      });
    }
  }

  render() {
    const { username, password, loggedIn, notification, images } = this.state;
    return (
      <div className="App">
        {loggedIn ?
          <Dashboard update={this.update} request={this.request} logout={this.logout} username={username} images={images} />
          : <Login update={this.update} request={this.request} username={username} password={password} />
        }
        {notification && <Notifications notification={notification} />}
      </div>
    );
  }
}

export default App;
