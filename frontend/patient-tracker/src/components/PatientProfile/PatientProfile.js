import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "reactstrap";
import "./PatientProfile.css";
import { useLocation } from "react-router-dom";

function PatientProfile() {
  //const [userId, setUserId] = useState(14);
  const location = useLocation();
  const state = location.state;
  const userId = state.userId;
  const patId = state.patId;
  const [patient, setPatient] = useState({});
  const [listFiles, setListFiles] = React.useState({});

  // communicate with backend to get user ID
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

        const response2 = await fetch("http://127.0.0.1:5000/get_file_urls", {
          method: "POST",
          mode: "cors",
          body: JSON.stringify({ patient_id: patId }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const result2 = await response2.json();
        setListFiles(result2);
      } catch (error) {
        alert(error);
      }
    };

    fetchDate();
  }, [userId]);

  return (
    // UIUX
    <div className="container">
      <div className="mt-3 nextApt">
        <h2> Patient Profile</h2>
      </div>
      <div className="info-card-pat-profile">
        <div className="patBox">
          <p>First Name: {patient.first_name}</p>
          <p>Last Name: {patient.last_name}</p>
          <p>Height (cm): {patient.height}</p>
          <p>Weight (kg): {patient.weight}</p>
          <p>Heart rate (bpm): </p>
          <p>Blood pressure:</p>
          <p>Date of birth: {patient.date_of_birth}</p>
          <p>
            Primary Care Physician: {patient.primary_care_doctor_first_name}{" "}
            {patient.primary_care_doctoc_last_name}
          </p>
        </div>
      </div>
      <h5 className="title">Documents</h5>

      <div className="list-files">
        {Object.keys(listFiles).length === 0 && (
          <div>
            <p>
              No documents for this patient yet!
            </p>
          </div>
        )}
        {Object.keys(listFiles).length > 0 && (
          <div>
            <ul className="list-group em_list">
              {Object.entries(listFiles).map(([filename, url]) => (
                <li className="list-group-item em btn">
                  <a href={url}>{filename}</a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientProfile;
