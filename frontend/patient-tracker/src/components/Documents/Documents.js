import React, { useState } from "react";
import axios from 'axios';
import './documents.css';
import { Button } from "reactstrap";
function Documents() {
   //let [file, setFile] = React.useState({selectedFile: null})
    let [files, setFiles] = React.useState([])
    const onFileChange = event => {
        console.log('eho')
        if (event.target.files[0]){
            console.log('helo')
            let target = event.target
            console.log('b4')
            console.log(files)
            setFiles(...target.files)
            console.log('after')
            console.log(files)
        }
    }
    const upload = ()=>{
        console.log('out')
        console.log(files)
        if (files.length > 0) {
            files.map((f) => {
                // Create an object of formData
                const formData = new FormData();
                console.log('formdata')
                // Update the formData object
                formData.append(
                    "myFile",
                    f,
                );
                console.log(formData)
                //axios.post("api/uploadfile", formData);
            })
        }
    }
    
    const update = () => {
        alert("update?");
    }

    const fileData = () => {
        if (files[0]) {
            return (
                <div className="list-container">
                    <ul className="list-group em_list">
                        {files.map((f)=> {
                            <div className="uploadedFileInfo">
                                <h3>File Detail:</h3>
                                <p>File Name: {f.name}</p>
                                <p>File Type: {f.type}</p>
                                <p>
                                    Last Modified:{" "}
                                    {f.lastModifiedDate}
                                </p>
                            </div>
                        })}
                    </ul>
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
        <div className='document'>
            <div className='buttons'>
                <div className = 'uploadButton'>
                    <input className="uploadFileInput" type="file" onChange={onFileChange} />
                    <Button onClick={upload}>Upload Medical Record</Button>
                </div>
                <Button onClick={update}>Manually Fill out Medical Record</Button>
            </div>
            {fileData()}
        </div>
    )
}

export default Documents;