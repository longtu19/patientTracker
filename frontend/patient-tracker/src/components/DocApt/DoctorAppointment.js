import React, { useState } from "react";
import "./doctorapt.css";
import { appoinments } from "./appointments.js";

function DoctorAppointment() {
  return (
    <div className="container justify-content-center align-items-center">
      <div className="mt-3 nextApt">
        <h2>Next Appointments</h2>
      </div>
      <div className="aptBox">
        <div className="list-container justify-content-center align-items-center">
          {appoinments.map((patient) => (
            <div className="card patientAptCard mt-3">
              <div class="card-header">
                {patient.first} {patient.last}
              </div>
              <div className="card-body text-start">
                <p className="card-text">Date: {patient.date}</p>
                <p className="card-text">From: {patient.from}</p>
                <p className="card-text">To: {patient.to}</p>
                <p className="card-text">DOB: {patient.dob}</p>
                <p className="card-text">Note: {patient.note}</p>
                <a href="#" class="btn btn-primary">
                  Patient Details
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DoctorAppointment;
