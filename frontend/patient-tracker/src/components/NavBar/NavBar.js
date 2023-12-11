import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";
import doctorGau from "../../Images/doctorGau.png";
import { useNavigate } from "react-router-dom";

function NavBar() {
  const navigate = useNavigate();
  const user_role = localStorage.getItem("user_role");
  const handleLogOut = () => {
    localStorage.removeItem("user_role");
    localStorage.removeItem("user_id");
    navigate("/");
  };
  return (
    <nav className="navbar-left">
      <img className="gaupic" src={doctorGau} />

      <ul>
        {user_role === "doctor" && (
          <li>
            <Link to="/doctorhome"> Doctor Home</Link>
          </li>
        )}
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
        {user_role !== null && <li>
          <Link to="/doctorappointment">Appointments</Link>
        </li>}
        {user_role === null && (
          <li>
            <Link to="/register">Create Account</Link>
          </li>
        )}
          {user_role === null && (
            <div>
            <li> 
              <Link to = "/documents"> Documents</Link>
            </li>
            <li>
              <Link to="/">Log In</Link>
            </li>
            <li>
              <Link to="/scheduler">Scheduler</Link>
            </li>
          </div>
        )}
      {user_role !== null &&  
        (<li>
          <button onClick={handleLogOut}>Log out</button>
        </li>)
        }

        {/* Add more navigation links */}
      </ul>
    </nav>
  );
}

export default NavBar;
