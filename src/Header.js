import React from 'react';
import './Header.css';

function Header() {
  return (
    <div className="Header">
      <div id="logo">
        <img src={`${process.env.PUBLIC_URL}/logo.png`} alt="Logo" />
      </div>
      <h2 className="Brand-Name">Interview-IQ</h2>
      <div className="profile-section">
        <div className="profile-pic">
          <img src={`${process.env.PUBLIC_URL}/user.png`} alt="Profile" />
        </div>
        <h3 className="Name">John Doe</h3>
      </div>
    </div>
  );
}

export default Header;