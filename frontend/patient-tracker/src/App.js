import logo from "./logo.svg";
import "./App.css";
import LogIn from "./components/LogIn/LogIn";
import DoctorHome from "./components/DoctorHome/DoctorHome";
import PatientHome from "./components/PatientHome/PatientHome";
import { BrowserRouter, Route, Routes } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <LogIn/>
          }
        />
        <Route path="/doctorHome" element={<DoctorHome />} />
        <Route path="/patientHome" element={<PatientHome />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
