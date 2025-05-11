import React from "react";
import Login from "../components/login";

const LoginPage = () => {
  return (
    <div className="  h-auto">
       <div className="flex justify-center mb-5">
        <img className="block w-[35px] lg:w-[40px] mr-1.5" src="/logo.svg" alt="Clyna Logo" />
        <h2 className="font-bold block text-center text-2xl text-primary">Clyna</h2>
       </div>
      <Login />
    </div>
  );
};

export default LoginPage;
