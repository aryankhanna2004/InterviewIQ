import React from 'react';
import './Header.css';

function Header() {
  return (
    <div className="Header">
      <h2 className="Brand-Name">Interview-IQ</h2>
      <div className="profile-section">
        <div className="profile-pic"></div>
        <h3 className="Name">John Doe</h3>
      </div>
    </div>
  );
}

export default Header;
