import React from 'react';
import './Notifications.css';

const Notifications = ({ notification }) => {
  const { message, type } = notification;
  return (
    <div className='Notifications'>
      <div className={`Notify animatedNotification ${type}`}>{message}</div>
    </div>
  );
};
export default Notifications;