import React from 'react';

const style = {
  display: 'inline-flex',
  verticalAlign: 'middle',
}

const Icon = ({ name }) => <span style={style} className="material-icons">{name}</span>;

export default Icon;