import logo from "./logo.svg";
import "./App.css";
import LogIn from "./components/LogIn/LogIn";
import Register from "./components/Register/Register";
import DoctorHome from "./components/DoctorHome/DoctorHome";
import PatientHome from "./components/PatientHome/PatientHome";
import DoctorAppointment from "./components/DocApt/DoctorAppointment";
import Documents from "./components/Documents/Documents";
import Scheduler from "./components/Scheduler/Scheduler";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar/NavBar";
import { Nav } from "reactstrap";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <NavBar/>
        <Routes>
          <Route path="/" element={<LogIn />} />
          <Route path="/register" element={<Register />} />
          <Route path="/doctorhome" element={<DoctorHome />} />
          <Route path="/doctorappointment" element={<DoctorAppointment />} />
          <Route path="/patienthome" element={<PatientHome />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/scheduler" element={<Scheduler />}/>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
