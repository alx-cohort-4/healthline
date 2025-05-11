import React from "react";
import { Outlet } from "react-router-dom";
import Nav from "../shared/Nav";
import image from "/images/ailayou.png";

const AuthLayout = () => {
  return (
    <div className="flex px-4 md:px-12 lg:px-25 flex-col min-h-dvh pb-20 ">
      {/* Header */}
      <Nav />
      {/* Main Content */}
      <div className="flex mt-35 lg:mt-25 border border-border-color overflow-hidden rounded-xl md:h-[100vh] h-auto ">
        <div className="max-md:hidden  w-auto  text-white md:w-1/2">
          <img
            src={image}
            loading="lazy"
            alt="Clyna"
            className="w-full h-full object-cover"
          />
        </div>
        <div className=" max-md:w-full max-md:shadow-md md:w-1/2 p-4 pt-12 px-10 flex flex-col  justify-center bg-white lg:p-10">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
