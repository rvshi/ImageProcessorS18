import React, { Component } from 'react';
import Menubar from './Menubar';
import './Dashboard.css';

// file reading
const MAX_FILE_SIZE = 1024 * 1024 * 4;
const SUPPORTED_FILE_TYPES = ['image/jpeg', 'image/png'];

class Dashboard extends Component {

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
      reader.onload = () => this.props.update('images', {
        ...this.props.images,
        original: reader.result
      }, () => this.props.request('upload'));
    }
  }

  render() {
    const { request, logout, username, images } = this.props;
    const req = {
      process: () => request('process'),
      downJPEG: () => request('download'),
      downPNG: () => request('download'),
    };

    return (
      <div className="Dashboard">
        <Menubar logout={logout} username={username} />

        <div className="Viewer">
          {images && <img src={images.original} alt="Original" />}

          <button onClick={this.upload}>Upload image</button>
          <button onClick={req.process}>Process image</button>
          <button onClick={req.downJPEG}>Download image as JPEG</button>
          <button onClick={req.downPNG}>Download image as PNG</button>
        </div>
        <input type="file" id="file" ref="imageUploader" onChange={(e) => this.handleFile(e.target.files)} style={{ display: "none" }} />
      </div>
    );
  }
}

export default Dashboard;
