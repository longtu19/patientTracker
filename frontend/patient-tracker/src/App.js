import logo from "./logo.svg";
import "./App.css";
import LogIn from "./components/LogIn/LogIn";
import Register from "./components/Register/Register";
import DoctorHome from "./components/DoctorHome/DoctorHome";
import PatientHome from "./components/PatientHome/PatientHome";
import Appointments from "./components/Appointments/Appointments";
import Documents from "./components/Documents/Documents";
import Scheduler from "./components/Scheduler/Scheduler";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar/NavBar";
import { Nav } from "reactstrap";
import ProtectedRoute from "../src/components/ProtectedRoute/ProtectedRoute";
import PrivateRoute from "./components/PrivateRoute/PrivateRoute";
import ListFiles from "./components/ListFiles/ListFiles";
import PatientProfile from "./components/PatientProfile/PatientProfile";

function App() {
  return (
    <BrowserRouter>
      <div className="App app-container">
        <NavBar />
        <div className="content-container">
          <Routes>
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<LogIn />} />
            </Route>
            <Route path="/register" element={<Register />} />

            {/* only available after logged in */}
            
            <Route element={<PrivateRoute />}>
              <Route path="/doctorhome" element={<DoctorHome />} />
              <Route path="/appointments" element={<Appointments />} />
              <Route path="/patienthome" element={<PatientHome />} />
              <Route path="/listfiles" element={<ListFiles />} />
              <Route path="/patientprofile" element={<PatientProfile />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="/scheduler" element={<Scheduler />} />
            </Route>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
