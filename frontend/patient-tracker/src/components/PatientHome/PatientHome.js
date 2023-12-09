import React, { useEffect, useState } from "react";
import axios from "axios";
import "./patient-home.css";
import { Button } from "reactstrap";
function upload() {
  alert("upload?");
}

function update() {
  alert("update?");
}

function PatientHome() {
  //const [userId, setUserId] = useState(14);
  const userId = localStorage.getItem("user_id");
  const [patient, setPatient] = useState({});
  useEffect(() => {
    const fetchDate = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get_patient_data", {
          method: "POST",
          mode: "cors",
          body: JSON.stringify({ user_id: userId }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const result = await response.json();
        console.log(result);
        if (result.Result === "Success") {
          setPatient(result.Data);
        }
      } catch (error) {
        alert(error);
      }
    };

    fetchDate()
  }, [userId]);



  return (
    <div>
      <div className="info-card">
        <div className="avatar">
          <img
            src="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg"
            alt="cat"
          />
        </div>
        <div className="info-text">
          <p>First Name: {patient.first_name}</p>
          <p>Last Name: {patient.last_name}</p>
          <p>Height: {patient.height}</p>
          <p>Weight: {patient.weight}</p>
          <p>Date of birth: {patient.date_of_birth}</p>
          <p>Primary Care Physician:</p>
        </div>
      </div>
      <div className="buttons">
        <Button onClick={update}>Manually Fill out Medical Record</Button>
      </div>
    </div>
  );
}

export default PatientHome;
