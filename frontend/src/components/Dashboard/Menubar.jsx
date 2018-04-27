import React from 'react';
import './Dashboard.css';

const Menubar = ({ logout, username }) => {

  return (
    <div className="Menubar">
      <h1>HYPERPIXEL</h1>
      <div className="info">
        <div className="username">{username}</div>
        <div className="interpunct">&#183;</div>
        <div className="logout" onClick={() => logout()}>logout</div>
      </div>
    </div>
  )
};

export default Menubar;
