import React, { Component } from 'react';
import Menubar from './Menubar';
import Icon from './Icon';
import './Dashboard.css';

// file reading
const MAX_FILE_SIZE = 1024 * 1024 * 4;
const FILE_TYPES = ['jpeg', 'png', 'gif'];
const SUPPORTED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
const filetype = 'jpeg';

class Dashboard extends Component {

  componentDidMount() {
    // download cloud images on first mount
    const { request } = this.props;
    this.props.list((data) => {
      const { originalID, processedID } = data;
      if (originalID != null) {
        request('download', { which: 'original', fileID: originalID, filetype });
      }
      if (processedID != null) {
        request('download', { which: 'processed', fileID: processedID, filetype });
      }
    });
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
      reader.onload = () => this.props.update('images', {
        ...this.props.images,
        original: reader.result
      }, () => this.props.request('upload'));
    }
  }

  render() {
    const { request, logout, username, images } = this.props,
      req = {
        process: () => request('process'),
        download: (which, type) => request('download', {
          which,
          fileID: images.processedID,
          filetype: type
        }, (file) => {
          const uploader = this.refs.imageDownloader;
          const fileName = `${images.processedID}.${type}`;
          uploader.setAttribute("href", file);
          uploader.setAttribute("download", fileName);
          uploader.click();
        })
      };

    return (
      <div className="Dashboard">
        <Menubar logout={logout} username={username} />

        <div className="Viewer">
          <div className="MainButtons">
            <button onClick={this.upload}>Upload image <Icon name="file_upload" /></button>
            {images.originalID && <button onClick={req.process}>Re-process image <Icon name="autorenew" /></button>}
          </div>

          {(images.original || images.processed) &&
            < div className="Images">
              {images.original && <img src={images.original} alt="Original" />}
              {images.processed && <img src={images.processed} alt="Processed" />}
            </div>}

          {images.originalID && <div className="Download"><Icon name="file_download" /> Download original as
            {FILE_TYPES.map((type, i) =>
              <button key={i} onClick={() => req.download('original', type)}>{type.toUpperCase()}</button>)}
          </div>}
          {images.processedID && <div className="Download"><Icon name="file_download" /> Download new as
            {FILE_TYPES.map((type, i) =>
              <button key={i} onClick={() => req.download('processed', type)}>{type.toUpperCase()}</button>)}
          </div>}

        </div>
        {/* Image upload element */}
        <input type="file" ref="imageUploader" onChange={(e) => this.handleFile(e.target.files)} style={{ display: "none" }} />
        {/* Image download element */}
        <a ref="imageDownloader" style={{ display: "none" }}>downloaded file</a>
      </div >
    );
  }
}

export default Dashboard;
