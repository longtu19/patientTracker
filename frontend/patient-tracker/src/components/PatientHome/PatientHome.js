import React, { useState } from "react";
import './patient-home.css'
import { Button } from "reactstrap";
function upload() {
    alert("upload?");
}

function update() {
    alert("update?");
}

function PatientHome(){
    return (
        <div>
            <div className='info-card'>
                    <div className='avatar'>
                        <img
                        src="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg" alt="cat" />
                    </div>
                    <div className='info-text'>
                        <p>Full Name:</p>
                        <p>Date of birth:</p>
                        <p>Height:</p>
                        <p>Weight:</p>
                    </div>
            </div>
            <div className='buttons'>
                <Button onClick={upload}>Upload Medical Record</Button>
                <Button onClick={update}>Update Medical Record</Button>
            </div>
        </div>
    )
}

export default PatientHome;


