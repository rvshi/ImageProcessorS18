import React, { Component } from 'react';
import { req, validate } from '../requests';
import Login from './Login';
import Dashboard from './Dashboard';
import Notifications from './Notifications';

const MAX_FILE_SIZE = 1024 * 1024 * 4;
const SUPPORTED_FILE_TYPES = ['image/jpeg', 'image/png'];
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

  update = (key, val) => {
    this.setState({ [key]: val });
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

  upload = () => {
    this.refs.imageUploader.click();
  }

  handleFile = (files) => {

    // validate file
    if (files.length === 1) {
      let file = files[0];
      if (file.size > MAX_FILE_SIZE) {
        this.notify('File is larger than 4MB', 'bad');
        return;
      } else if (!SUPPORTED_FILE_TYPES.includes(file.type)) {
        this.notify('File must be JPEG or PNG', 'bad');
        return;
      }

      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.setState({
          images: {
            original: reader.result
          }
        });
      };
    }
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
    const { username, password, loggedIn, notification, images } = this.state;
    return (
      <div className="App">
        {loggedIn ?
          <Dashboard update={this.update} request={this.request} logout={this.logout} username={username} upload={this.upload} images={images} />
          : <Login update={this.update} request={this.request} username={username} password={password} />
        }
        {notification && <Notifications notification={notification} />}

        <input type="file" id="file" ref="imageUploader" onChange={(e) => this.handleFile(e.target.files)} style={{ display: "none" }} />
      </div>
    );
  }
}

export default App;
