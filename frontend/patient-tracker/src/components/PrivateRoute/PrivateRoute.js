import { Navigate, Outlet, Route } from "react-router-dom";
// only accessible when logged in, redirect to login page if not
const PrivateRoute = () => {
    const isAuth = !!localStorage.getItem("user_id")
    return isAuth ? <Outlet/> : <Navigate to = "/"/>
}

export default PrivateRoute;