import React, { useEffect, useState } from "react";
import axios from 'axios';
import './patient-home.css'
import { Button } from "reactstrap";
function upload() {
    alert("upload?");
}

function update() {
    alert("update?");
}

function PatientHome(){
    const [userId, setUserId] = useState(14);
    const [patient, setPatient] = useState({});
    useEffect(async () => {
        const response = await fetch("http://127.0.0.1:5000/get_patient_data", {
            method: "GET",
            mode: "cors",
            body: JSON.stringify({ userId: userId }),
            headers: {
              "Content-Type": "application/json",
            },

        });
        const result = await response.json();
        if (result.Result === "Success"){
            setPatient(result.Data);
        }


    })
    let [file, setFile] = React.useState({selectedFile: null})
    const onFileChange = event => {
        setFile({ selectedFile: event.target.files[0] });
    }
    const onFileUpload = () => {
        // Create an object of formData
        const formData = new FormData();
 
        // Update the formData object
        formData.append(
            "myFile",
            file.selectedFile,
            file.selectedFile.name
        );
 
        // Details of the uploaded file
        console.log(file.selectedFile);
 
        // Request made to the backend api
        // Send formData object
        axios.post("api/uploadfile", formData);
    };

    const fileData = () => {
        if (file.selectedFile) {
            return (
                <div className="uploadedFileInfo">
                    <h3>File Detail:</h3>
                    <p>File Name: {file.selectedFile.name}</p>
                    <p>File Type: {file.selectedFile.type}</p>
                    <p>
                        Last Modified:{" "}
                        {file.selectedFile.lastModifiedDate.toDateString()}
                    </p>
 
                </div>
            );
        } else {
            return (
                <div className="uploadedFileInfo">
                </div>
            );
        }
    };

    return (
        <div>
            <div className='info-card'>
                    <div className='avatar'>
                        <img
                        src="https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg" alt="cat" />
                    </div>
                    <div className='info-text'>
                        <p>First Name: {patient.first_name}</p>
                        <p>Last Name: {patient.last_name}</p>
                        <p>Height: {patient.height}</p>
                        <p>Weight: {patient.weight}</p>
                        <p>Date of birth: {patient.date_of_birth}</p>
                        <p>Primary Care Physician:</p>
                    </div>
            </div>
            <div className='buttons'>
                <div className = 'uploadButton'>
                    <input className="uploadFileInput" type="file" onChange={onFileChange} />
                    <Button onClick={upload}>Upload Medical Record</Button>
                </div>
                {fileData()}
                <Button onClick={update}>Manually Fill out Medical Record</Button>
            </div>
        </div>
    )
}

export default PatientHome;


