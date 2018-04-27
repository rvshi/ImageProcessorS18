import React from 'react';
import Menubar from './Menubar';
import './Dashboard.css';

const Dashboard = ({ request, update, logout, username, upload, images }) => {
  images && console.log(images['original']);

  return (
    <div className="Dashboard">
      <Menubar logout={logout} username={username} />

      <div className="Viewer">
        {images && <img src={images.original} alt="Original" />}

        <button onClick={upload}>Upload image</button>
        <button>Reprocess image</button>
        <button>Download image as JPEG</button>
      </div>
    </div>
  )
};

export default Dashboard;
