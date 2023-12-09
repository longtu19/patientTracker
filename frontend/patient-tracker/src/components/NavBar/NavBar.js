import React from "react";
import { Link } from 'react-router-dom';
import './navbar.css'
import doctorGau from "../../Images/doctorGau.png"


function NavBar() {
  return (
    <nav className="navbar-left">
      <img className = "gaupic"src = {doctorGau}/>
    
      <ul>
        <li>
          <Link to="/doctorhome"> Doctor Home</Link>
        </li>
        <li>
          <Link to="/patienthome"> Patient Home</Link>
        </li>
        <li>
          <Link to="/doctorappointment">Appointments</Link>
        </li>
        <li>
          <Link to="/register">Create Account</Link>
        </li>
        <li> 
        <Link to = "/documents"> Documents</Link>
        </li>
        <li>
          <Link to="/">Log Out</Link>
        </li>
        <li>
          <Link to="/scheduler">Scheduler</Link>
        </li>
      
  
        {/* Add more navigation links */}
      </ul>
    </nav>
  );
}

export default NavBar;
