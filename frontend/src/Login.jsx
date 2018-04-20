import React, { Component } from 'react';
import './Login.css';

const Login = ({ request, update, email, password }) => (
    <div className="Login">
        <div className="Login-circle">
            <h1>Super Pixel </h1>
            <h2>Welcome to the future of image segmentation.</h2>

            <input type="text" placeholder="username" autoComplete="off" autoFocus value={email} onChange={e => update('email', e.target.value)} />
            <input type="password" placeholder="password" autoComplete="off" value={password} onChange={e => update('password', e.target.value)} />
            <button type="submit" onClick={() => request('login')}>login</button>
        </div>
    </div>
);

export default Login;
