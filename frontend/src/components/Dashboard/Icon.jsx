import React from 'react';

const style = {
  display: 'inline-flex',
  verticalAlign: 'middle',
}

const Icon = ({ name }) => <span style={style} class="material-icons">{name}</span>;

export default Icon;