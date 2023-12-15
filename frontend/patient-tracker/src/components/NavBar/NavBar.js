import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";
import doctorGau from "../../Images/doctorGau.png";
import { useNavigate } from "react-router-dom";

function NavBar() {
  const navigate = useNavigate();
  const user_role = localStorage.getItem("user_role");
  const handleLogOut = () => {
    localStorage.clear()
    navigate("/");
  };
  return (
    <nav className="navbar-left">
      <img className="gaupic" src={doctorGau} />

      <ul>

      {/* only show for doctor */}
        {user_role === "doctor" && (
          <li>
            <Link to="/doctorhome"> Doctor Home</Link>
          </li>
        )}
        
        {/* only show for patient */}
        {user_role === "patient" && (
          <li>
            <Link to="/patienthome"> Patient Home</Link>
          </li>
        )}
        {user_role === "patient" && (
          <li>
            <Link to="/listfiles"> Documents</Link>
          </li>
        )}
        {user_role === "patient" && (
          <li>
            <Link to="/scheduler"> Scheduler</Link>
          </li>
        )}
        {user_role !== null && (
          <li>
            <Link to="/appointments">Appointments</Link>
          </li>
        )}
        {user_role === null && (
          <li>
            <Link to="/register">Create Account</Link>
          </li>
        )}
        {user_role === null && (
          <li>
            <Link to="/"> Log In </Link>
          </li>
        )}
        {user_role !== null && (
          <li>
            <button onClick={handleLogOut}>Log out</button>
          </li>
        )}
      </ul>
    </nav>
  );
}

export default NavBar;
