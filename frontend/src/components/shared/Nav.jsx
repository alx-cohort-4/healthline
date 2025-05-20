import React from "react";
import { X, Menu } from "lucide-react";
import { useState } from "react";
import { LogoIcon } from "../../globals/Icons";
import Button from "../ui/Button";
import { useNavigate, useLocation } from "react-router-dom";
const Nav = () => {
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const toggleNarbar = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };
  const navigate = useNavigate();
  const location = useLocation();
  const hideAuthButtons = ["/login", "/signup"].includes(location.pathname);
  const navItems = [
    { label: "Features", href: "#features" },
    { label: "How it works", href: "#how-it-works" },
    { label: "Contact Us", href: "#contact-us" },
  ];

  return (
    <nav className="w-full bg-white text-primary flex items-center justify-between px-4 md:px-12 lg:px-20 py-2 fixed top-0 left-0 shadow-md z-50">
      <div
        onClick={() => {
          navigate("/");
        }}
        className="flex cursor-pointer items-center gap-2 mb-4"
      >
        <LogoIcon className=" max-md:w-20 max-md:h-8  " />
      </div>

      <ul className="hidden lg:flex space-x-6 items-center">
        {navItems.map((item) => (
          <li
            key={item.label}
            className="hover:bg-[#e6f0ff] px-3 py-2 rounded cursor-pointer active:bg-[#cce0ff]"
          >
            <a href={item.href}>{item.label}</a>
          </li>
        ))}
      </ul>
      {!hideAuthButtons && (
        <div className="hidden lg:flex space-x-4">
          <>
            <Button
              onClick={() => {
                navigate("/login");
              }}
              className="px-4 py-2  hover:bg-transparent bg-transparent hover:text-primary/80 text-primary"
            >
              Login
            </Button>
            <Button
              onClick={() => {
                navigate("/signup");
              }}
              className="px-4 py-2 bg-primary text-white rounded"
            >
              Sign Up
            </Button>
          </>
        </div>
      )}

      <button
        className="lg:hidden text-3xl font-bold text-primary hover:bg-[#e6f0ff] px-3 py-2 rounded z-[60]"
        onClick={toggleNarbar}
      >
        {mobileDrawerOpen ? <X /> : <Menu />}
      </button>

      {mobileDrawerOpen && (
        <div className="fixed bg-black/50 right-0 -top-5 z-50 mt-20 w-full h-full   flex flex-col justify-start items-start lg:hidden">
          <div className="bg-white w-full h-auto  md:p-12  p-6 flex flex-col justify-start items-start">
            <ul className="space-y-6 text-left w-full">
              {navItems.map((item) => (
                <li
                  key={item.label}
                  className="hover:bg-[#e6f0ff] px-3 py-2 rounded cursor-pointer active:bg-[#cce0ff]"
                >
                  <a href={item.href}>{item.label}</a>
                </li>
              ))}
            </ul>
            {!hideAuthButtons && (
              <div className="flex flex-col space-y-4 w-[100%] mt-8">
                <button
                  className="w-full px-4 py-2 text-primary border border-primary rounded"
                  onClick={() => navigate("/login")}
                >
                  Login
                </button>
                <button
                  className="w-full px-4 py-2 bg-primary text-white rounded"
                  onClick={() => navigate("/signup")}
                >
                  Sign Up
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Nav;
