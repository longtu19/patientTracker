import React, { useState } from "react";
import "./LogIn.css";
import Cookies from "js-cookie";

function ForgotPassword() {
  return (
    <div className="wait ">
      Please contact admin at payranger@duckcreek.com!
    </div>
  );
}

export default function LogIn(props) {
  Cookies.remove("isLoggedIn");
  Cookies.remove("userLoggedIn");




  return (
    <div className="loginbg">
      <div className="login_wrapper">
        <div className="loginFlexbox justify-content-center align-items-center ">
          <h1>Login</h1>
          <div className="ip">
            <input
              type="text"
              placeholder="Username"
            />
          </div>

          <div className="ip">
            <input
              type="password"
              placeholder="Password"
            />
          </div>

          <button className="loginButton" >
            Login
          </button>
          <button className="createAccButton" >
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
