import logo from "./logo.svg";
import "./App.css";
import LogIn from "./components/LogIn/LogIn";
import Register from "./components/Register/Register";
import DoctorHome from "./components/DoctorHome/DoctorHome";
import PatientHome from "./components/PatientHome/PatientHome";
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
          <Route path="/doctorHome" element={<DoctorHome />} />
          <Route path="/patientHome" element={<PatientHome />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
