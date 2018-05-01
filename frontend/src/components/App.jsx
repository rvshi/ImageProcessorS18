import React, { Component } from 'react';
import { get, post } from '../requests';
import Login from './Login';
import Dashboard from './Dashboard';
import Notifications from './Notifications';

const defaultState = {
  username: '',
  password: '',
  jwt: null,
  loggedIn: false,
  images: {}
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
      get(jwt, 'validate', (res, success) => {
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

  // list items
  list = (cb) => {
    const { jwt, images } = this.state;
    get(jwt, 'list', (res, success) => {
      if (success) {
        const data = res.data;
        this.setState({ images: { ...images, ...data } });
        cb(data);
      }
    });
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
    this.notify('Logged out successfully', 'good');
  }

  request = (path, options, cb) => {
    const { jwt, username, password, images } = this.state;

    if (path === 'login') {
      post(null, path, { username, password }, (res, success) => {
        if (success) {
          const jwt = res.data.jwt;
          localStorage.setItem('jwt', jwt);
          this.setState({ 'jwt': jwt, 'loggedIn': true });
          this.notify(`Welcome back ${username}!`, 'good');
        } else {
          this.notify('Username or password are incorrect.', 'bad');
        }
      });
    } else if (path === 'upload' && options) {
      const { original } = options;
      post(jwt, path, { username, file: original }, (res, success) => {
        if (success) {
          const originalID = res.data.fileID;
          this.setState({ images: { ...images, original, originalID } });
          this.notify('Image uploaded', 'good');
          this.request('process');
        } else {
          this.notify('Error uploading image.', 'bad');
        }
      });
    } else if (path === 'process') {
      post(jwt, path, { username }, (res, success) => {
        if (success) {
          const processedID = res.data.fileID;
          this.setState({ images: { ...images, processedID } });
          this.notify(`Image processed`, 'good');
          this.request('download', { which: 'processed', fileID: processedID, filetype: 'jpeg' });
        } else {
          this.notify('Error processing image.', 'bad');
        }
      });
    } else if (path === 'download' && options) {
      const { which, fileID, filetype } = options;
      post(jwt, path, { username, fileID, filetype }, (res, success) => {
        if (success) {
          const file = res.data.file;
          if (file) {
            const imgFile = `data:image/${filetype};base64,${file}`
            if (cb) {
              cb(imgFile);
            } else {
              this.setState({
                images:
                  Object.assign({}, this.state.images, {
                    [which]: imgFile
                  })
              });
            }
          } else { // handle case where images are deleted from server
            this.setState({
              images:
                Object.assign({}, this.state.images, {
                  [which]: null,
                  [which + 'ID']: null
                })
            });
          }
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
          <Dashboard update={this.update} request={this.request} logout={this.logout} username={username} images={images} list={this.list} />
          : <Login update={this.update} request={this.request} username={username} password={password} />
        }
        {notification && <Notifications notification={notification} />}
      </div>
    );
  }
}

export default App;
