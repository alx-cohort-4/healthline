import React from "react";
import { Outlet } from "react-router-dom";
import Nav from "../shared/Nav";

const AuthLayout = () => {
  return (
    <div className="flex px-25 flex-col min-h-screen">
      {/* Header */}
      <Nav />
      {/* Main Content */}
      <div className="flex mt-25 min-h-[85vh] h-auto ">
        <div className="bg-secondary rounded-xl grid place-content-center  text-white w-1/2">
          AI HealthLine
        </div>
        <div className="w-1/2 bg-white p-8">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
