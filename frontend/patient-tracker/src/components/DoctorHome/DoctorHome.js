import * as React from "react";
import { useEffect, useState } from "react";
import "./doctorhome.css";
import { patients } from "./patients_db";
import { v4 as uuid } from "uuid";
import { useNavigate, Link } from "react-router-dom";
import PatientProfile from "../PatientProfile/PatientProfile";
import {
  Button,
  Form,
  FormGroup,
  Input,
  Label,
  Modal,
  ModalHeader,
  ModalBody,
} from "reactstrap";

export default function DoctorHome() {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  const [searchQuery, setSearchQuery] = React.useState("");

  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false);
  let [firstname, setFirstname] = React.useState("");
  let [lastname, setLastname] = React.useState("");
  let [datevalue, setDate] = React.useState("");
  let [patLst, setPatLst] = React.useState([]);
  let [selectedPat, setSelectedPat] = React.useState(null);

  useEffect(() => {
    const fetchDate = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/get_patients_by_doctor_id",
          {
            method: "POST",
            mode: "cors",
            body: JSON.stringify({ user_id: userId }),
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        const result = await response.json();
        console.log(result);
        if (result.Result === "Success") {
          if (result.Data !== null) {
            setPatLst(result.Data);
            console.log(patLst);
          }
        }
      } catch (error) {
        alert(error);
      }
    };

    fetchDate();
  }, [userId]);

  const filteredPat = patLst.filter(
    (item) =>
      item[0].toLowerCase().includes(searchQuery.toLowerCase()) ||
      item[1].toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelectPat = (userId, firstName, lastName) => {
    setSelectedPat({
      userId: userId,
      firstName: firstName,
      lastName: lastName,
    });
    navigate('/patientprofile', { state: { userId: userId } });

  };

  const handleSearchQueryChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
  };

  // const toggleModal = () => {
  //   setIsModalOpen(!isModalOpen);
  // };

  // const toggleAddModal = () => {
  //   setIsAddModalOpen(!isAddModalOpen);
  // };

  // const closeBtn = (
  //   <button className="close " onClick={toggleModal} type="button">
  //     &times;
  //   </button>
  // );

  return (
    <div className="homebg">
      <div className="container d-flex justify-content-center align-items-center  ">
        <div className="employeeBox justify-content-center align-items-center  ">
          <div>
            <div className="mb-2 d-flex " style={{ color: "#162938" }}>
              <h2>Patients</h2>
            </div>

            <form className="d-flex srch-parent" role="search">
              <input
                className="form-control me-2 em_search"
                type="search"
                placeholder="Search a patient"
                aria-label="Search"
                value={searchQuery}
                onChange={handleSearchQueryChange}
              ></input>
              <button
                className="btn srch-btn"
                type="submit"
                onClick={handleSearchSubmit}
              >
                Search
              </button>
            </form>

            <div className="  d-flex justify-content-center ">
              <div className="list-container">
                {filteredPat.length === 0 && (
                  <div>No patients assigned yet!</div>
                )}
                <ul className="list-group em_list">
                  {filteredPat &&
                    filteredPat.map((pat) => (
                      <li className="list-group-item em btn">
                        <Link to="/patientprofile" state={{ userId: pat[2] }}>
                          {pat[0]} {pat[1]}
                          </Link>
                      </li>
                    ))}
                </ul>
              </div>
            </div>

            <div className="metric mt-5 ">
              <button className="btn count-btn" type="submit">
                Patients Counted: {patLst.length}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
