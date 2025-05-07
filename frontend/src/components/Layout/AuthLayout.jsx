import React from "react";
import { Outlet } from "react-router-dom";
import Nav from "../shared/Nav";

const AuthLayout = () => {
  return (
    <div className="flex px-4 md:px-12 lg:px-25 flex-col min-h-dvh pb-20 ">
      {/* Header */}
      <Nav />
      {/* Main Content */}
      <div className="flex mt-25 border border-border-color overflow-hidden rounded-xl md:min-h-[85vh] h-auto ">
        <div className="bg-secondary max-md:hidden grid place-content-center w-auto  text-white md:w-1/2">
          AI HealthLine
        </div>
        <div className=" max-md:w-full max-md:shadow-md md:w-1/2 p-4 flex flex-col  justify-center   bg-white lg:p-8">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
