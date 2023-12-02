import * as React from "react";
import { useEffect, useState } from "react";
import "./doctorhome.css";
import { patients } from "./patients_db";
import { v4 as uuid } from "uuid";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";
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
  const userId = localStorage.getItem("user_id");

  const [searchQuery, setSearchQuery] = React.useState("");

  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = React.useState(false);
  let [firstname, setFirstname] = React.useState("");
  let [lastname, setLastname] = React.useState("");
  let [datevalue, setDate] = React.useState("");
  let [patLst, setPatLst] = React.useState(patients);
  let [selectedPat, setSelectedPat] = React.useState(null);
  let [count, setCount] = React.useState(patLst.length);


  useEffect(() => {
    const fetchDate = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get_patients_by_doctor_id", {
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
          setPatLst(result.Data);
        }
      } catch (error) {
        alert(error);
      }
    };

    fetchDate()
  }, [userId]);

  const filteredPat = patLst.filter(
    (item) =>
      item.first.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.last.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelectEmp = (empId, firstName, lastName) => {
    setSelectedPat({
      employeeId: empId,
      firstName: firstName,
      lastName: lastName,
    });
    setIsModalOpen(!isModalOpen);
  };

  const handleSearchQueryChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
  };

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  const toggleAddModal = () => {
    setIsAddModalOpen(!isAddModalOpen);
  };

  const closeBtn = (
    <button className="close " onClick={toggleModal} type="button">
      &times;
    </button>
  );

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
                <ul className="list-group em_list">
                  {filteredPat.map((pat) => (
                    <li className="list-group-item em btn">
                      <p>
                        {pat.first} {pat.last}
                      </p>
                    </li>
                  ))}
                </ul>

                {selectedPat && (
                  <Modal
                    isOpen={isModalOpen}
                    toggle={toggleModal}
                    className="my-emp-modal"
                  >
                    <ModalHeader
                      toggle={toggleModal}
                      className="modal-head"
                      close={closeBtn}
                    >
                      {selectedPat.firstName + " " + selectedPat.lastName}
                    </ModalHeader>
                  </Modal>
                )}
              </div>
            </div>

            <div className="metric mt-5 ">
              <button className="btn count-btn" type="submit">
                Patients Counted: {count}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
