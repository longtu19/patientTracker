import React, { useState } from "react";
import "./LogIn.css";
import Cookies from "js-cookie";
import { BrowserRouter, Route, useNavigate } from "react-router-dom";

export default function LogIn(props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const onPasswordChange = (event) => {
    setPassword(event.target.value);
  };




  const navigate = useNavigate();
  const handleLogin = async () => {

    const response = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ email: email, password: password }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log('Here')
    const user = await response.json();
   
    if (user.Result === 'Success') {

      navigate("/patienthome");

      

      // set user context to authenticated
    } else {
      alert("Login or password is incorrect. If you forgot your password, contact your administrator.")
    }
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div className="loginbg">
      <div className="login_wrapper">
        <div className="loginFlexbox justify-content-center align-items-center ">
          <h1>Login</h1>
          <div className="ip">
            <input type="text" placeholder="Email" onChange={onEmailChange} />
          </div>

          <div className="ip">
            <input type="password" placeholder="Password" onChange={onPasswordChange}/>
          </div>

          <button className="loginButton" onClick={handleLogin}>
            Login
          </button>
          <button className="createAccButton" onClick={handleRegister}>
            Create Account
          </button>

          <div className="mt-4 ">
            <a href="#" class="forgotpw">
              Forgot password?
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
