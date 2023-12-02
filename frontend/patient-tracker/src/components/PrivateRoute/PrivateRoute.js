import { Navigate, Outlet, Route } from "react-router-dom";

const PrivateRoute = () => {
    const isAuth = !!localStorage.getItem("user_id")
    return isAuth ? <Outlet/> : <Navigate to = "/"/>
}

export default PrivateRoute;