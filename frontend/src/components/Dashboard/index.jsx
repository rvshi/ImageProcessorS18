import React from 'react';
import Menubar from './Menubar';
import './Dashboard.css';

const Dashboard = ({ request, update, logout, username, password }) => (
  <div className="Dashboard">
    <Menubar logout={logout} username={username} />

    <div className="ImageViewer">
      <div>Image</div>

      <button>Load image</button>
      <button>Process image</button>
      <button>Download image as JPEG</button>
    </div>
  </div>
);

export default Dashboard;
