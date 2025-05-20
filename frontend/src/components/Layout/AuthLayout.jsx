import React from "react";
import { Outlet, Link } from "react-router-dom";
import Nav from "../shared/Nav";
import image from "/images/auth-image.png";
import { LogoIcon, LogoIconFlip } from "../../globals/Icons";
import { useNavigate } from "react-router-dom";

const AuthLayout = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen">
      <div className="md:hidden">
        <Nav />
      </div>

      <div className="flex max-md:mt-[4rem] flex-col md:flex-row  ">
        <div className="max-md:w-full max-md:order-1 max-md:rounded-2xl bg-wite  overflow-hidden md:w-1/2 max-md:flex-1 p-4 md:px-10 flex flex-col">
          <Link
            to="/"
            className="flex max-md:hidden cursor-pointer items-center gap-2 mb-4"
          >
            <LogoIcon className=" max-md:w-20 max-md:h-8" />
          </Link>
          <div className="flex-1">
            <Outlet />
          </div>
        </div>
        <div className="text-white max-md:bg-primary max-md:flex max-md:items-center max-md:justify-center h-[33vh] md:h-screen md:w-1/2   md:sticky  md:top-0">
          <div
            onClick={() => {
              navigate("/");
            }}
            className="flex md:hidden cursor-pointer items-center gap-2 mb-4"
          >
            <LogoIconFlip className="w-10 h-10" />
            <div>
              <span className="font-bold block text-center text-lg lg:text-[22px]">
                Clyna
              </span>
            </div>
          </div>
          <img
            src={image}
            alt="Clyna"
            className="h-full max-md:hidden w-full object-center "
          />
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
