import React, { useEffect, useState } from "react";
import axios from "axios";
import "./listFiles.css";
import { Button } from "reactstrap";
function upload() {
  alert("upload?");
}

function update() {
  alert("update?");
}

function ListFiles() {
  //const [userId, setUserId] = useState(14);
  const roleId = localStorage.getItem("role_id");
  console.log(roleId);

  const [file, setFile] = useState(null);
  const [listFiles, setListFiles] = React.useState({});
  const [uploadTrigger, setUploadTrigger] = useState(false); // New state variable

  useEffect(() => {
    const fetchDate = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get_file_urls", {
          method: "POST",
          mode: "cors",
          body: JSON.stringify({ patient_id: roleId }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const result = await response.json();
        setListFiles(result);
      } catch (error) {
        alert(error);
      }
    };

    fetchDate();
  }, [roleId, uploadTrigger]);

  const handleUploadFile = async (formData) => {
    const response = await fetch("http://127.0.0.1:5000/upload_file", {
      method: "POST",
      mode: "cors",
      body: formData,
    });
    const user = await response.json();
    if (user.Result === "Success") {
      alert("Successfully uploaded file");
      setUploadTrigger(!uploadTrigger);
    } else {
      alert("Failed to upload file. Please try again.");
    }
  };

  const onFileChange = (event) => {
    // setFile(event.target.files[0]);
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      let formData = new FormData();
      formData.append("record", selectedFile);
      formData.append("patient_id", roleId);
      handleUploadFile(formData);
    }
  };

  return (
    <div className="container ">
      <div className="list-files">
        {Object.keys(listFiles).length === 0 && (
          <div>
            <p>
              No documents uploaded yet! Use the button below to upload one.
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
        <div className="buttons">
          <div className="uploadButton">
            <input
              className="uploadFileInput"
              type="file"
              onChange={onFileChange}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default ListFiles;
