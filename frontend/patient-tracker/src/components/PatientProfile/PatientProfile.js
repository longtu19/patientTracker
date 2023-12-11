import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "reactstrap";
import "./PatientProfile.css"
import { useLocation } from "react-router-dom";

function PatientProfile() {
  //const [userId, setUserId] = useState(14);
  const location = useLocation();
  console.log(location)
  const state = location.state;
  const userId = state.userId ;
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

    fetchDate();
  }, [userId]);

  return (
    <div>
      <div className="info-card">
        <div className="patBox">
          <p>First Name: {patient.first_name}</p>
          <p>Last Name: {patient.last_name}</p>
          <p>Height: {patient.height}</p>
          <p>Weight: {patient.weight}</p>
          <p>Date of birth: {patient.date_of_birth}</p>
          <p>
            Primary Care Physician: {patient.primary_care_doctor_first_name}{" "}
            {patient.primary_care_doctoc_last_name}
          </p>
        </div>
      </div>
    </div>
  );
}

export default PatientProfile;
