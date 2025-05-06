import React from "react";
import { X, Menu } from "lucide-react";
import { useState } from "react";

const Nav = () => {
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const toggleNarbar = () => {
    setMobileDrawerOpen(!mobileDrawerOpen);
  };

  const navItems = [
    { label: "Features", href: "#features" },
    { label: "How it works", href: "#how-it-works" },
    { label: "Contact Us", href: "#contact-us" },
  ];

  return (
    <nav className="w-full bg-white text-primary flex items-center justify-between px-4 md:px-12 lg:px-25 py-4 fixed top-0 left-0 shadow-md z-50">
      <div className="text-xl font-bold z-[60]">AI HealthLine</div>

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

      {/* <div className="hidden lg:flex space-x-4">
        <button className="px-4 py-2 text-primary">Login</button>
        <button className="px-4 py-2 bg-primary text-white rounded">Sign Up</button>
      </div> */}

      <button
        className="lg:hidden text-3xl font-bold text-primary hover:bg-[#e6f0ff] px-3 py-2 rounded z-[60]"
        onClick={toggleNarbar}
      >
        {mobileDrawerOpen ? <X /> : <Menu />}
      </button>

      {mobileDrawerOpen && (
        <div className="fixed right-0 top-0 z-[55] bg-white w-full h-[25rem] mt-20 p-12 flex flex-col justify-start items-start lg:hidden">
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
          <div className="flex flex-col space-y-4 w-[100%] mt-8">
            <button className="w-full px-4 py-2 text-primary border border-primary rounded">
              Login
            </button>
            <button className="w-full px-4 py-2 bg-primary text-white rounded">
              Sign Up
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Nav;
