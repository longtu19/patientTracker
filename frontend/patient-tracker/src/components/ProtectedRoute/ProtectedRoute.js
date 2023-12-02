import React from 'react';
import { Route, Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
  const loggedIn = localStorage.getItem("user_id");
  const role = localStorage.getItem("user_role")
  if (loggedIn !== null){
    if (role === "patient"){
        return <Navigate to = "/patienthome"/>
    }
    else {
        return <Navigate to = "/doctorhome"/>

    }
  }
  else {
    return <Outlet />
  }


};

export default ProtectedRoute;
