import React from 'react';

const Nav = () => {
  return (
    <nav className="w-full bg-white text-[#175cd3] flex items-center justify-between px-6 py-4 fixed top-0 left-0 shadow-md z-50">
      
      <div className="text-xl font-bold">AI HealthLine</div>

      
      <ul className="flex space-x-6">
        <li className="hover:bg-[#e6f0ff] px-3 py-2 rounded cursor-pointer active:bg-[#cce0ff]">Features</li>
        <li className="hover:bg-[#e6f0ff] px-3 py-2 rounded cursor-pointer active:bg-[#cce0ff]">How it works</li>
        <li className="hover:bg-[#e6f0ff] px-3 py-2 rounded cursor-pointer active:bg-[#cce0ff]">Contact Us</li>
      </ul>

      
      <div className="flex space-x-4">
        <button className="px-4 py-2 text-[#175cd3]">Login</button>
        <button className="px-4 py-2 bg-[#175cd3] text-white rounded">Sign Up</button>
      </div>
    </nav>
  );
};

export default Nav;