import React, { useState, useEffect } from "react";
import "./apt.css";

function Appointments() {
  const [aptDetails, setAptDetails] = useState([]);
  const roleId = localStorage.getItem("role_id");
  const patFName = localStorage.getItem("patFName");
  const patLName = localStorage.getItem("patLName");
  const docFName = localStorage.getItem("docFName");
  const docLName = localStorage.getItem("docLName");
  const user_role = localStorage.getItem("user_role");

  useEffect(() => {
    const fetchDate = async () => {
      if (user_role === "patient") {
        try {
          const response = await fetch(
            "http://127.0.0.1:5000/get_appointments_by_patient_id",
            {
              method: "POST",
              mode: "cors",
              body: JSON.stringify({ patient_id: roleId }),
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          const result = await response.json();
          console.log(result);
          if (result.Result === "Success") {
            setAptDetails(result.Appointments);
            console.log(result.Appointments);
          }
        } catch (error) {
          alert(error);
        }
      } else {
        try {
          const response = await fetch(
            "http://127.0.0.1:5000/get_appointments_by_doctor_id",
            {
              method: "POST",
              mode: "cors",
              body: JSON.stringify({ doctor_id: roleId }),
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          const result = await response.json();
          console.log(result);
          if (result.Result === "Success") {
            setAptDetails(result.Appointments);
            console.log(result.Appointments);
          }
        } catch (error) {
          alert(error);
        }
      }
    };

    fetchDate();
  }, [roleId]);

  return (
    <div className="container justify-content-center align-items-center">
      <div className="mt-3 nextApt">
        <h2> Upcoming Appointments</h2>
      </div>
      <div className="aptBox">
        <div className="list-container justify-content-center align-items-center">
          {aptDetails.map((apt) => (
            <div className="card patientAptCard mt-3">
              <div class="card-header">
                {patFName} {patLName}
              </div>
              <div className="card-body text-start">
                <p className="card-text">Start Time: {apt[4]}</p>
                <p className="card-text">End Time: {apt[5]}</p>
                <p className="card-text">
                  Doctor: {docFName} {docLName}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Appointments;
