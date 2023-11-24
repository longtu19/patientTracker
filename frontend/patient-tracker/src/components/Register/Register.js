import React, { useState } from "react";
import "./../LogIn/LogIn.css";
import Cookies from "js-cookie";
import { BrowserRouter, Route, useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState(null);
  const [firstName, setFirstName] = useState(null);
  const [lastName, setLastName] = useState(null);
  const [password, setPassword] = useState(null);
  const [role, setRole] = useState(null);
  const [birthday, setBirthday] = useState(null);
  const [sex, setSex] = useState(null);

  const handleEmail = event => {
    setEmail(event.target.value);
    console.log(email)
  }

  const handlePassword= event => {
    setPassword(event.target.value);
    console.log(password)
  }

  const handleSex = e => {
    setSex(e.target.value)
  }


  const navigate = useNavigate();
  const handleRegister = async () => {

    const response = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({ 
        email: email, 
        password: password, 
        first_name:firstName, 
        last_name: lastName, 
        role: role, 
        birthday: birthday,
        sex: sex
       }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const user = await response.json();
    console.log(user)
    if (response.ok) {
      alert("Congrats!! Your account has been created")

      navigate("/");

      

      // set user context to authenticated
    } else {
      alert("Login or password is incorrect. If you forgot your password, contact your administrator.")
    }
  };

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  return (
    <div className="loginbg">
      <div className="login_wrapper">
        <div className="createAccBox justify-content-center align-items-center ">
          <h1>Create Account</h1>

          <div className="role">
            <div className="youare">You are</div>

            <div className="form-check form-check-inline option1 ">
              <input class="form-check-input" type="radio" value="patient" name="role" onChange={handleRoleChange} />
              <label className="form-check-label" for="inlineCheckbox1"> A Patient </label>
            </div>
            <div className="form-check form-check-inline">
              <input class="form-check-input" type="radio" value="doctor" name="role" onChange={handleRoleChange} />
              <label className="form-check-label" for="inlineCheckbox2"> A Doctor </label>
            </div>
          </div>

    

          <div className="ip">
            <input type="text" placeholder="First Name" onChange={e => setFirstName(e.target.value)} />
          </div>

          <div className="ip">
            <input type="text" placeholder="Last Name"  onChange={e => setLastName(e.target.value)}/>
          </div>
       

          <div className="ip">
            <input type="text" placeholder="Email" onChange={handleEmail} />
          </div>
          <div className="ip">
            <input type="password" placeholder="Password" onChange={handlePassword} />
          </div>

          {role === "patient" && (
            <div className="ip">
              <input type="text" name="dob" placeholder="Birthday mm/dd/yyyy" pattern="\d{4}-\d{2}-\d{2}" onChange={e => setBirthday(e.target.value)} required/>
            </div>
          )}



          {role === "patient" && <div className="role">
            <div className="sex">Sex</div>
            <div className="sex-choices">
              <div className="form-check form-check-inline ">
                <input class="form-check-input" type="radio" value="male" name="sex" onChange={handleSex} />
                <label className="form-check-label" for="inlineCheckbox1"> Male </label>
              </div>
              <div className="form-check form-check-inline">
                <input class="form-check-input" type="radio" value="female" name="sex" onChange = {handleSex}/>
                <label className="form-check-label" for="inlineCheckbox2"> Female </label>
              </div>
              <div className="form-check form-check-inline">
                <input class="form-check-input" type="radio" value="other" name="sex" onChange = {handleSex} />
                <label className="form-check-label" for="inlineCheckbox2"> Other </label>
              </div>
            </div>
          </div>}

          <button className="createAccButton mt-4" onClick={handleRegister}>Create Account</button>
        </div>
      </div>
    </div>
  );
}
