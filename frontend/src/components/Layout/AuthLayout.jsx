import React from "react";
import { Outlet } from "react-router-dom";
import Header from "../shared/Header";

const AuthLayout = () => {
  return (
    <div className="flex px-25 flex-col min-h-screen">
      {/* Header */}
      <Header />
      {/* Main Content */}
      <div className="flex  min-h-[85vh] h-auto ">
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
