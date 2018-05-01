import React from 'react';
import './Login.css';

const Login = ({ request, update, username, password }) => (
    <div className="Login">
        <div className="Login-circle">
            <h1>HYPERPIXEL</h1>
            <h2>Corneal image segmentation, made easy.</h2>

            <input type="text" placeholder="username" autoComplete="off" autoFocus value={username} onChange={e => update('username', e.target.value)} />
            <input type="password" placeholder="password" autoComplete="off" value={password} onChange={e => update('password', e.target.value)} />
            <button type="submit" onClick={() => request('login')}>login</button>
        </div>
    </div>
);

export default Login;
