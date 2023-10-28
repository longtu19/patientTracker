import React from "react";
import { Link } from 'react-router-dom';
import './navbar.css'


function NavBar() {
  return (
    <nav className="navbar-left">
      <ul>
        <li>
          <Link to="/doctorHome">Home</Link>
        </li>
        <li>
          <Link to="/">Log Out</Link>
        </li>
  
        {/* Add more navigation links */}
      </ul>
    </nav>
  );
}

export default NavBar;
